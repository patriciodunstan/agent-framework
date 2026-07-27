from framework.model import ConfigError, InstallReport, OutputFile


def test_outputfile_is_frozen():
    f = OutputFile("CLAUDE.md", "hola")
    assert f.relpath == "CLAUDE.md"
    assert f.content == "hola"


def test_installreport_defaults_empty():
    r = InstallReport()
    assert r.created == [] and r.skipped == [] and r.warnings == []


def test_configerror_is_exception():
    assert issubclass(ConfigError, Exception)
