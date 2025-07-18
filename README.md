# Lispy

Lispy is an ultra-minimal Lisp kernel intended for bootstrapping a self-hosted Lisp system. It aims to be just large enough to provide a minimal Turing complete core with which additional Lisp features can be built. The emphasis is on clarity and small size rather than performance or extensive libraries.

## Design Goals

- **Tiny core**: keep the implementation small and easy to inspect.
- **Self-hosting**: provide enough primitives to implement the rest of the language in itself.
- **Portability**: only depend on a small subset of the host system (ideally ANSI C).
- **Understandability**: favor simple algorithms and transparent design over cleverness.

## Core Components

The kernel is expected to contain just the essentials required for a Lisp interpreter:

1. **Reader/Parser** – converts textual s-expressions into internal data structures.
2. **Evaluator** – a minimal eval loop with support for symbols, lists, numbers, and basic special forms.
3. **Environment** – a mapping of symbols to values, including primitive functions and user-defined bindings.
4. **Garbage Collection** – optional; for the initial kernel a simple mark-and-sweep or reference counting collector may be used.

## Initial Feature Set

Below is a checklist of the minimal functionality Lispy aims to provide. As
features are implemented, they can be ticked off here to track progress.

- [x] Numbers, symbols, lists, and basic cons operations (`cons`, `car`, `cdr`).
- [x] Definition and invocation of simple functions (`lambda`, `defun`).
- [x] Conditionals (`if`) and sequential execution (`progn`).
- [x] Basic arithmetic primitives.
- [x] Limited macro facility to support bootstrapping.
- [x] Ability to execute Lispy code from a file.
- [ ] A small standard library written in Lispy itself once the core is
  operational.

## Usage

Run the interpreter directly with Python:

```bash
python3 lispy.py
```

You can also run a Lispy source file by passing it as an argument:

```bash
python3 lispy.py path/to/program.lisp
```

You'll be dropped into a REPL prompt where you can enter Lisp forms:

```lisp
lispy> (+ 1 2)
3
```

## Future Work

This project is still in its early stages. Future commits will expand the standard library, add more tests, and improve the documentation.

