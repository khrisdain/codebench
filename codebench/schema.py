import json
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = ("id", "category", "entry_point", "prompt", "tests")

class SchemaError(ValueError):
    """Raised when a benchmark file is malformed."""

@dataclass(frozen=True)
class Item:
    id: str
    category: str
    entry_point: str
    prompt: str
    tests: tuple[str, ...]

def load_items(path: Path) -> list[Item]:
    items: list[Item] = []
    seen: set[str] = set()
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SchemaError(f"line {line_no}: invalid JSON ({exc.msg})") from exc
        missing = [f for f in REQUIRED_FIELDS if f not in raw]
        if missing:
            raise SchemaError(f"line {line_no}: missing fields {missing}")
        if not raw["tests"]:
            raise SchemaError(f"line {line_no}: item {raw['id']} has no tests")
        if raw["id"] in seen:
            raise SchemaError(f"line {line_no}: duplicate id {raw['id']}")
        seen.add(raw["id"])
        items.append(Item(raw["id"], raw["category"], raw["entry_point"], raw["prompt"], tuple(raw["tests"])))
    return items