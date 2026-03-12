"""Filesystem state snapshots with diff comparison."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path


__all__ = [
    "snapshot",
    "Snapshot",
    "SnapshotDiff",
    "FileEntry",
]


@dataclass(frozen=True)
class FileEntry:
    """Metadata for a single file in a snapshot."""

    path: str
    size: int
    mtime: float
    hash: str | None = None


@dataclass
class SnapshotDiff:
    """Result of comparing two snapshots."""

    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        """Whether any files were added, removed, or modified."""
        return bool(self.added or self.removed or self.modified)

    def summary(self) -> str:
        """Return a human-readable summary of changes."""
        parts: list[str] = []
        if self.added:
            parts.append(f"{len(self.added)} added")
        if self.removed:
            parts.append(f"{len(self.removed)} removed")
        if self.modified:
            parts.append(f"{len(self.modified)} modified")
        if self.unchanged:
            parts.append(f"{len(self.unchanged)} unchanged")
        return ", ".join(parts) if parts else "Empty snapshot"


@dataclass
class Snapshot:
    """A point-in-time snapshot of a directory's file state."""

    path: str
    files: dict[str, FileEntry] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def file_count(self) -> int:
        """Number of files in the snapshot."""
        return len(self.files)

    def diff(self, other: Snapshot) -> SnapshotDiff:
        """Compare this snapshot against an older snapshot.

        Args:
            other: The previous snapshot to compare against.

        Returns:
            SnapshotDiff with added, removed, modified, and unchanged files.
        """
        result = SnapshotDiff()
        all_paths = set(self.files) | set(other.files)

        for path in sorted(all_paths):
            if path not in self.files:
                result.added.append(path)
            elif path not in other.files:
                result.removed.append(path)
            else:
                old = other.files[path]
                new = self.files[path]
                if old.hash is not None and new.hash is not None:
                    if old.hash != new.hash:
                        result.modified.append(path)
                    else:
                        result.unchanged.append(path)
                elif old.size != new.size or old.mtime != new.mtime:
                    result.modified.append(path)
                else:
                    result.unchanged.append(path)

        return result

    def to_json(self, path: str | Path | None = None) -> str:
        """Serialize the snapshot to a JSON string, optionally writing to a file.

        Args:
            path: If provided, write the JSON to this file path.

        Returns:
            The JSON string.
        """
        data = {
            "path": self.path,
            "created_at": self.created_at,
            "files": {k: asdict(v) for k, v in self.files.items()},
        }
        result = json.dumps(data, indent=2)
        if path is not None:
            Path(path).write_text(result, encoding="utf-8")
        return result

    @classmethod
    def from_json(cls, data: str) -> Snapshot:
        """Deserialize a snapshot from a JSON string or file path."""
        p = Path(data)
        if p.exists() and p.is_file():
            data = p.read_text(encoding="utf-8")
        parsed = json.loads(data)
        files = {
            k: FileEntry(**v)
            for k, v in parsed["files"].items()
        }
        return cls(
            path=parsed["path"],
            files=files,
            created_at=parsed["created_at"],
        )


def snapshot(
    path: str | Path,
    hash_mode: str = "mtime",
    include: str | list[str] | None = None,
    exclude: str | list[str] | None = None,
) -> Snapshot:
    """Capture the current state of a directory.

    Args:
        path: Directory path to snapshot.
        hash_mode: ``"mtime"`` for fast size+mtime comparison, or
            ``"sha256"`` for content-based hashing.
        include: Glob pattern to include only matching files.
        exclude: Glob pattern to exclude matching files.

    Returns:
        A Snapshot of all files in the directory.
    """
    root = Path(path).resolve()
    if not root.is_dir():
        msg = f"Not a directory: {root}"
        raise NotADirectoryError(msg)

    files: dict[str, FileEntry] = {}

    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue

        relative = str(file_path.relative_to(root)).replace("\\", "/")

        if include:
            patterns = [include] if isinstance(include, str) else include
            if not any(fnmatch(relative, p) for p in patterns):
                continue
        if exclude:
            patterns = [exclude] if isinstance(exclude, str) else exclude
            if any(fnmatch(relative, p) for p in patterns):
                continue

        stat = file_path.stat()
        file_hash: str | None = None

        if hash_mode == "sha256":
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            file_hash = h.hexdigest()

        files[relative] = FileEntry(
            path=relative,
            size=stat.st_size,
            mtime=stat.st_mtime,
            hash=file_hash,
        )

    return Snapshot(path=str(root), files=files)
