import json

import pytest

from codebench.schema import Item

@pytest.fixture
def add_item():
    return Item(id="t-001", category="math", entry_point="add", prompt="Add two numbers.", tests=("assert add(2, 3) == 5", "assert add(-1, 1) == 0"))


@pytest.fixture
def write_items(tmp_path):
    def _write(rows):
        path = tmp_path / "items.jsonl"
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        return path
    return _write


@pytest.fixture
def solution(tmp_path):
    def _solution(code, name="t-001.py"):
        path= tmp_path / name
        path.write_text(code)
        return path
    return _solution 



