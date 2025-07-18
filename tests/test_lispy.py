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
