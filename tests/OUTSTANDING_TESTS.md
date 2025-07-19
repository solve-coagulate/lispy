# Outstanding Test Ideas

The current Lispy test suite covers a variety of core features, but there are still areas that would benefit from additional tests. Below is a list of future test ideas:

- ~~**Arithmetic**: subtraction, multiplication and division with both integers and floats.~~
- ~~**Comparisons**: `<`, `<=` and `>=` forms with different numeric types.~~
- ~~**`list` construction**: nested lists and quoting behaviour.~~
- ~~**Multiple-argument lambdas**: ensure parameters bind correctly and closures capture values.~~
- ~~**`macroexpand`**: verify that macros expand fully and correctly.~~
- ~~**Error handling**: undefined symbols, invalid forms and wrong arity errors.~~
- ~~**`progn` sequencing**: confirm side effects occur in order.~~
- **File loading**: running multiple Lisp source files in sequence.
- ~~**Printing**: capturing the output of the `print` primitive.~~

These tests can be added incrementally as the interpreter evolves.
