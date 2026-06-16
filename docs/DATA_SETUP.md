# Data Setup

Raw SCRUPLES anecdote files are not included in this public repository. This is intentional: redistribution should be confirmed against the dataset license, provider terms, privacy considerations, and ethics review before publishing raw text.

To run data-dependent tests and real milestone planning, place the SCRUPLES anecdote split files here:

```text
data/scruples/anecdotes/
  train.scruples-anecdotes.jsonl
  dev.scruples-anecdotes.jsonl
  test.scruples-anecdotes.jsonl
```

The public test suite skips data-dependent tests when these files are absent. Core protocol, metric, parsing, configuration, and schema tests still run without raw data.

Before provider execution, confirm:

- the files are from the intended SCRUPLES Anecdotes version;
- local paths are not committed if raw redistribution is not allowed;
- generated `runs/` outputs and SQLite ledgers remain ignored unless intentionally released.
