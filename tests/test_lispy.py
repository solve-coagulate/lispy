import subprocess
import sys
from pathlib import Path


def run_lispy(source: str) -> str:
    script = Path(__file__).with_name('tmp.lisp')
    script.write_text(source)
    exe = Path(__file__).resolve().parents[1] / 'lispy.py'
    output = subprocess.check_output([sys.executable, str(exe), str(script)])
    script.unlink()
    return output.decode().strip()


def test_run_file():
    out = run_lispy('(define x 41)\n(+ x 1)')
    assert out == '42'


def test_lisp_test_suite():
    source = """
(define failures 0)

(define assert-eq
  (lambda (name actual expected)
    (if (= actual expected)
        (progn (print (quote PASS) name) nil)
        (progn (print (quote FAIL) name (quote expected) expected (quote got) actual)
               (define failures (+ failures 1))
               nil))))

(assert-eq (quote addition) (+ 1 1) 2)
(assert-eq (quote car) (car (list 1 2 3)) 1)
(if (= failures 0) 0 1)
"""
    out = run_lispy(source)
    assert out.splitlines()[-1] == '0'
