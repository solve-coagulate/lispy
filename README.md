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

- [ ] Numbers, symbols, lists, and basic cons operations (`cons`, `car`, `cdr`).
- [ ] Definition and invocation of simple functions (`lambda`, `defun`).
- [ ] Conditionals (`if`) and sequential execution (`progn`).
- [ ] Basic arithmetic primitives.
- [ ] Limited macro facility to support bootstrapping.
- [ ] A small standard library written in Lispy itself once the core is
  operational.

## Future Work

This repository currently contains only this documentation and the license. The actual implementation of Lispy is yet to be committed. Future commits will flesh out the interpreter, tests, and more comprehensive documentation.

