from codebench.runner import ERROR, FAILED, MISSING, PASSED, TIMEOUT, run_item, run_model

def test_correct_solution_passes(add_item, solution):
    result = run_item(add_item, solution("def add(a, b):\n   return a + b\n"))
    assert result.status == PASSED


def test_wrong_answer_fails(add_item, solution):
    result = run_item(add_item, solution("def add(a, b):\n  return a - b\n"))
    assert result.status == FAILED
    assert "assert add(2, 3) == 5" in result.detail


def test_syntax_error_is_an_error_not_a_failure(add_item, solution):
    result = run_item(add_item, solution("def add(a, b)\n   return a + b\n"))
    assert result.status == ERROR
    assert "SyntaxError" in result.detail


def test_exception_during_test_is_an_error(add_item, solution):
    result = run_item(add_item, solution("def add(a, b):\n  raise ValueError('boom')\n"))
    assert result.status == ERROR
    assert "ValueError" in result.detail


def test_infinite_loop_times_out(add_item, solution):
    result = run_item(add_item, solution("def add(a, b):\n        while True:\n        pass\n"), timeout=0.5)
    assert result.status == TIMEOUT

def test_missing_solution_file(add_item, tmp_path):
    result = run_item(add_item, tmp_path / "nope.py")
    assert result.status == MISSING


def test_solution_cannot_exist_early_and_fake_a_pass(add_item, solution):
    result = run_item(add_item, solution("import sys\nsys.exit(0)\n"))
    assert result.status != PASSED


def test_run_model_keeps_item_order(add_item, tmp_path):
    (tmp_path / "t-001.py").write_text("def add(a, b):\n    return a + b\n")
    results = run_model([add_item, add_item], tmp_path)
    assert [r.item_id for r in results] == ["t-001", "t-001"]
