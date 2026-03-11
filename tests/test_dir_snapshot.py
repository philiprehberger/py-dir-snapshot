import json
import tempfile
from pathlib import Path
from philiprehberger_dir_snapshot import snapshot, Snapshot


def test_snapshot_empty_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        snap = snapshot(tmpdir)
        assert len(snap.files) == 0


def test_snapshot_with_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.txt").write_text("hello")
        (Path(tmpdir) / "b.txt").write_text("world")
        snap = snapshot(tmpdir)
        assert len(snap.files) == 2


def test_snapshot_diff_no_changes():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.txt").write_text("hello")
        snap1 = snapshot(tmpdir)
        snap2 = snapshot(tmpdir)
        diff = snap1.diff(snap2)
        assert not diff.has_changes


def test_snapshot_diff_added():
    with tempfile.TemporaryDirectory() as tmpdir:
        snap1 = snapshot(tmpdir)
        (Path(tmpdir) / "new.txt").write_text("new")
        snap2 = snapshot(tmpdir)
        diff = snap1.diff(snap2)
        assert diff.has_changes
        assert len(diff.added) == 1


def test_snapshot_diff_removed():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = Path(tmpdir) / "old.txt"
        f.write_text("old")
        snap1 = snapshot(tmpdir)
        f.unlink()
        snap2 = snapshot(tmpdir)
        diff = snap1.diff(snap2)
        assert len(diff.removed) == 1


def test_snapshot_diff_modified():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = Path(tmpdir) / "file.txt"
        f.write_text("v1")
        snap1 = snapshot(tmpdir)
        f.write_text("v2")
        snap2 = snapshot(tmpdir)
        diff = snap1.diff(snap2)
        assert len(diff.modified) == 1


def test_to_json_and_from_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.txt").write_text("hello")
        snap = snapshot(tmpdir)
        json_path = str(Path(tmpdir) / "snap.json")
        snap.to_json(json_path)
        loaded = Snapshot.from_json(json_path)
        assert len(loaded.files) == len(snap.files)


def test_include_filter():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.py").write_text("code")
        (Path(tmpdir) / "b.txt").write_text("text")
        snap = snapshot(tmpdir, include=["*.py"])
        assert len(snap.files) == 1


def test_exclude_filter():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.py").write_text("code")
        (Path(tmpdir) / "b.pyc").write_bytes(b"\x00")
        snap = snapshot(tmpdir, exclude=["*.pyc"])
        assert len(snap.files) == 1


def test_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "a.txt").write_text("v1")
        snap1 = snapshot(tmpdir)
        (Path(tmpdir) / "a.txt").write_text("v2")
        (Path(tmpdir) / "b.txt").write_text("new")
        snap2 = snapshot(tmpdir)
        diff = snap1.diff(snap2)
        summary = diff.summary()
        assert isinstance(summary, str)
