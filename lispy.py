#!/usr/bin/env python3
"""A minimal Lisp interpreter for bootstrapping.

This interpreter intentionally implements only the bare essentials
needed for a Turing complete Lisp.  It is inspired by Peter Norvig's
"lispy" interpreter but trimmed down for clarity.
"""

import operator as op
import sys
from typing import Any, Iterable, List

Symbol = str
ListType = list
Number = (int, float)


def _print_lisp(*args: Any) -> None:
    """Primitive print function for Lispy."""
    def _to_string(exp: Any) -> str:
        if isinstance(exp, list):
            return '(' + ' '.join(map(_to_string, exp)) + ')'
        return str(exp)

    print(' '.join(_to_string(a) for a in args))


class Env(dict):
    """Environment mapping symbols to values."""

    def __init__(self, params: Iterable[Symbol] = (), args: Iterable[Any] = (), outer: 'Env' = None) -> None:
        super().__init__(zip(params, args))
        self.outer = outer

    def find(self, var: Symbol) -> 'Env':
        if var in self:
            return self
        if self.outer is None:
            raise NameError(var)
        return self.outer.find(var)


class Procedure:
    """User-defined Lisp procedure."""

    def __init__(self, params: List[Symbol], body: Any, env: Env, is_macro: bool = False) -> None:
        self.params = params
        self.body = body
        self.env = env
        self.is_macro = is_macro

    def __call__(self, *args: Any) -> Any:
        local_env = Env(self.params, args, self.env)
        return eval_lisp(self.body, local_env)


def standard_env() -> Env:
    """Create an environment with some Scheme standard procedures."""
    env = Env()
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'null?': lambda x: x == [],
        'symbol?': lambda x: isinstance(x, str),
        'progn': lambda *x: x[-1] if x else None,
        'print': _print_lisp,
        'nil': None,
    })
    return env


global_env = standard_env()


def parse(program: str) -> Any:
    """Read a Lisp expression from a string."""
    return read_from_tokens(tokenize(program))


def parse_multiple(program: str) -> List[Any]:
    """Parse multiple expressions from a string."""
    tokens = tokenize(program)
    exps = []
    while tokens:
        exps.append(read_from_tokens(tokens))
    return exps


def tokenize(s: str) -> List[str]:
    """Convert a string into a list of tokens."""
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens: List[str]) -> Any:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L: List[Any] = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token: str) -> Any:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def eval_lisp(x: Any, env: Env = global_env) -> Any:
    """Evaluate an expression in an environment."""
    while True:
        if isinstance(x, Symbol):      # variable reference
            return env.find(x)[x]
        elif not isinstance(x, ListType):  # constant literal
            return x
        op_sym = x[0]
        if op_sym == 'quote':          # (quote exp)
            (_, exp) = x
            return exp
        elif op_sym == 'if':           # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval_lisp(test, env) else alt)
            continue
        elif op_sym == 'define':       # (define var exp)
            (_, var, exp) = x
            env[var] = eval_lisp(exp, env)
            return None
        elif op_sym == 'lambda':       # (lambda (var...) body)
            (_, params, body) = x
            return Procedure(params, body, env)
        elif op_sym == 'progn':        # (progn exp...)
            for exp in x[1:-1]:
                eval_lisp(exp, env)
            x = x[-1]
            continue
        elif op_sym == 'defmacro':     # (defmacro name (args) body)
            (_, name, params, body) = x
            proc = Procedure(params, body, env, is_macro=True)
            env[name] = proc
            return None
        elif op_sym == 'macroexpand':  # (macroexpand exp)
            (_, exp) = x
            return macroexpand(exp, env)
        elif op_sym == 'try':          # (try exp) -> True if error
            (_, exp) = x
            try:
                eval_lisp(exp, env)
                return False
            except Exception:
                return True
        else:                          # (proc arg...)
            proc = eval_lisp(op_sym, env)
            if isinstance(proc, Procedure) and proc.is_macro:
                x = proc(*x[1:])
                continue
            else:
                args = [eval_lisp(arg, env) for arg in x[1:]]
                if isinstance(proc, Procedure):
                    return proc(*args)
                else:
                    return proc(*args)


def macroexpand(x: Any, env: Env) -> Any:
    """Recursively expand macros until expression no longer changes."""
    while isinstance(x, ListType) and isinstance(eval_lisp(x[0], env), Procedure) and eval_lisp(x[0], env).is_macro:
        proc = eval_lisp(x[0], env)
        x = proc(*x[1:])
    return x


def repl(prompt: str = 'lispy> ') -> None:
    """A simple read-eval-print loop."""
    while True:
        try:
            val = eval_lisp(parse(input(prompt)))
            if val is not None:
                print(to_string(val))
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except Exception as e:
            print('Error:', e)


def run_file(path: str, env: Env = global_env) -> None:
    """Execute a file containing Lispy expressions."""
    with open(path) as f:
        program = f.read()
    result = None
    for exp in parse_multiple(program):
        result = eval_lisp(exp, env)
    if result is not None:
        print(to_string(result))


def to_string(exp: Any) -> str:
    """Convert a Python object back into a Lisp-readable string."""
    if isinstance(exp, ListType):
        return '(' + ' '.join(map(to_string, exp)) + ')'
    else:
        return str(exp)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for fname in sys.argv[1:]:
            run_file(fname)
    else:
        repl()
