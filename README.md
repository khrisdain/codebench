# codebench

Seed data for a function-level code generation benchmark.

- `benchmark/items.jsonl`: 32 problems across 4 categories (strings, math, lists, dicts). Each has a prompt, an entry point and hidden tests.
- `baselines/<model>/<item-id>.py`: one solution file per item for three model outputs: `reference`, `model_a`, `model_b`.

The harness that runs and scores these is built in `codebench/`.
