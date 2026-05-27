# Changelog

## 0.3.0 (2026-05-26)

- Add `Snapshot.verify()` returning a `VerifyReport` — re-checks every stored entry against disk to confirm files still exist and content matches. Useful for backup verification and tamper detection.
- Add package-card image to README

## 0.2.3 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.2.2

- Convert API section to table format
- Document FileEntry, SnapshotDiff.has_changes, and SnapshotDiff field lists

## 0.2.1

- Add pytest and mypy tool configuration to pyproject.toml

## 0.2.0

- Trim keywords to match pyproject template guide

## 0.1.6

- Add Development section to README

## 0.1.3

- Fix from_json to accept file path argument

## 0.1.2

- Fix diff added/removed being swapped
- Fix to_json to accept optional file path
- Fix include/exclude filters to accept list of patterns

## 0.1.1

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)

- Initial release
- Directory state capture with file metadata
- Snapshot diff showing added/removed/modified
- Hash modes: mtime (fast) and sha256 (accurate)
- JSON export/import for persistence
