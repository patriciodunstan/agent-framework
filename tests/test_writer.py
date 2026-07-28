from framework.model import InstallReport, OutputFile
from framework.writer import ensure_line, write_tree


def test_write_tree_creates_and_reports(tmp_path):
    files = [OutputFile("a/b.txt", "hola"), OutputFile("c.txt", "mundo")]
    report = write_tree(tmp_path, files, InstallReport())
    assert (tmp_path / "a" / "b.txt").read_text(encoding="utf-8") == "hola"
    assert set(report.created) == {"a/b.txt", "c.txt"}


def test_write_tree_is_idempotent(tmp_path):
    files = [OutputFile("a.txt", "v1")]
    write_tree(tmp_path, files, InstallReport())
    report2 = write_tree(tmp_path, [OutputFile("a.txt", "v2")], InstallReport())
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "v1"  # no se pisa
    assert report2.skipped == ["a.txt"]
    assert report2.created == []


def test_ensure_line_creates_then_noop(tmp_path):
    gi = tmp_path / ".gitignore"
    report = InstallReport()
    ensure_line(gi, ".claude/", report)
    ensure_line(gi, ".claude/", report)
    assert gi.read_text(encoding="utf-8").count(".claude/") == 1
