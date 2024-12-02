# philiprehberger-dir-snapshot

[![Tests](https://github.com/philiprehberger/py-dir-snapshot/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-dir-snapshot/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-dir-snapshot.svg)](https://pypi.org/project/philiprehberger-dir-snapshot/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-dir-snapshot)](https://github.com/philiprehberger/py-dir-snapshot/commits/main)

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

| Function / Class | Description |
|------------------|-------------|
| `snapshot(path, hash_mode="mtime", include=None, exclude=None)` | Create a directory snapshot |
| `Snapshot.diff(other)` | Compare two snapshots, returns `SnapshotDiff` |
| `Snapshot.to_json(path)` / `Snapshot.from_json(path)` | Serialize/deserialize |
| `FileEntry` | File metadata — `.path`, `.size`, `.mtime`, `.hash` |
| `SnapshotDiff.has_changes` | `True` if any files were added, removed, or modified |
| `SnapshotDiff.added` / `.removed` / `.modified` / `.unchanged` | Lists of file paths |
| `SnapshotDiff.summary()` | Human-readable diff summary |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-dir-snapshot)

🐛 [Report issues](https://github.com/philiprehberger/py-dir-snapshot/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-dir-snapshot/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
