import pytest

from codebench.schema import SchemaError, load_items

VALID = {"id": "a-1", "category": "math", "entry_point": "f", "prompt": "p", "tests": ["assert f()"]}

def test_loads_valid_items(write_items):
    items = load_items(write_items([VALID, {**VALID, "id": "a-2"}]))
    assert [i.id for i in items] == ["a-1", "a-2"]
    assert items[0].tests == ("assert f()",)

def test_rejects_missing_fields(write_items):
    row = {k: v for k, v in VALID.items() if k != "entry_point"}
    with pytest.raises(SchemaError, match="entry_point"):
        load_items(write_items([row]))

def test_rejects_duplicate_ids(write_items):
    with pytest.raises(SchemaError, match="duplicate id a-1"):
        load_items(write_items([VALID, VALID]))

def test_rejects_items_without_tests(write_items):
    with pytest.raises(SchemaError, match="no tests"):
        load_items(write_items([{**VALID, "tests": []}]))

def test_reports_line_number_for_bad_json(tmp_path):
    path= tmp_path / "items.jsonl"
    path.write_text('{"id": "ok"}\n{not json\n')
    with pytest.raises(SchemaError, match="line 1|line 2"):
        load_items(path)

