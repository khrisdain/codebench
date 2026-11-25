import subprocess
import sys 
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from .schema import Item

PASSED, FAILED, ERROR, TIMEOUT, MISSING = "passed", "failed", "error", "timeout", "missing"

#Exist codes used by the generated check script
EXIT_FAILED, EXIT_TEST_ERROR, EXIT_LOAD_ERROR = 1, 2, 3

CHECK_TEMPLATE = '''\
import sys
SOLUTION = {solution!r}
TESTS= {tests!r}
try:
    exec(compile(SOLUTION, "solution.py", "exec"), globals())
except BaseException as exc:
    print(f"load error: {{type(exc).__name__}}: {{exc}}", file=sys.stderr)
    sys.exit({load_error})
for test in TESTS:
    try:
        exec(test, globals())
    except AssertionError:
        print(f"failed: {failed}: {{test}}", file=sys.stderr)
        sys.exit({failed})
    except BaseException as exc:
        print(f"error in {{test}}: {{type(exc).__name__}}: {{exc}}", file=sys.stderr)
        sys.exit({test_error})
'''

@dataclass
class Result:
    item_id: str
    category: str
    status: str
    duration_s: float
    detail: str = ""


def run_item(item: Item, solution_path: Path, timeout: float = 2.0) -> Result:
    if not solution_path.exists():
        return Result(item.id, item.category, MISSING, 0.0, f"no file at {solution_path}")

    script = CHECK_TEMPLATE.format(
        solution=solution_path.read_text(), tests=list(item.tests),
        load_error= EXIT_LOAD_ERROR, failed=EXIT_FAILED, test_error=EXIT_TEST_ERROR,
    )
    start = time.perf_counter()
    with tempfile.TemporaryDirectory() as tmp:
        check = Path(tmp) / "check.py"
        check.write_text(script)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(check)],
                cwd=tmp, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return Result(item.id, item.category, TIMEOUT, timeout, f"exceeded {timeout}s")
        duration = round(time.perf_counter() - start, 3)
        detail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""

        if proc.returncode == 0:
            status = PASSED
        elif proc.returncode == EXIT_FAILED:
            status = FAILED
        else:
            status = ERROR
        return Result(item.id, item.category, status, duration, detail)

def run_model(items: list[Item], solutions_dir: Path, timeout: float = 2.0,workers: int = 8) -> list[Result]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [ pool.submit(run_item, item, solutions_dir / f"{item.id}.py", timeout) for item in items]
        return [f.result() for f in futures]