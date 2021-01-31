# philiprehberger-dir-snapshot

[![Tests](https://github.com/philiprehberger/py-dir-snapshot/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-dir-snapshot/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-dir-snapshot.svg)](https://pypi.org/project/philiprehberger-dir-snapshot/)
[![License](https://img.shields.io/github/license/philiprehberger/py-dir-snapshot)](LICENSE)

Filesystem state snapshots with diff comparison.

## Installation

```bash
pip install philiprehberger-dir-snapshot
```

## Usage

### Take a Snapshot

```python
from philiprehberger_dir_snapshot import snapshot

snap = snapshot("./src")
print(f"Found {len(snap.files)} files")
```

### Compare Snapshots

```python
before = snapshot("./src")
# ... make changes ...
after = snapshot("./src")

diff = before.diff(after)
print(diff.summary())

for f in diff.added:
    print(f"+ {f.path}")
for f in diff.removed:
    print(f"- {f.path}")
for f in diff.modified:
    print(f"~ {f.path}")
```

### Save and Load

```python
# Save to JSON
before.to_json("snapshot.json")

# Load later
from philiprehberger_dir_snapshot import Snapshot
restored = Snapshot.from_json("snapshot.json")
```

### Options

```python
# Include only Python files
snap = snapshot("./src", include=["*.py"])

# Exclude build artifacts
snap = snapshot(".", exclude=["__pycache__", "*.pyc", ".git"])

# Use faster hashing (or disable with "none")
snap = snapshot(".", hash_mode="md5")
```

## API

- `snapshot(path, hash_mode="sha256", include=None, exclude=None)` — Create a snapshot
- `Snapshot.diff(other)` — Compare two snapshots, returns `SnapshotDiff`
- `Snapshot.to_json(path)` / `Snapshot.from_json(path)` — Serialize/deserialize
- `SnapshotDiff.summary()` — Human-readable diff summary

## License

MIT
