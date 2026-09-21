import json

from check_coverage import main


def _write_report(tmp_path, totals):
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"totals": totals}))
    return str(report)


def test_both_metrics_pass(tmp_path):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 96,
            "num_statements": 100,
            "covered_branches": 96,
            "num_branches": 100,
        },
    )

    assert main([report]) == 0


def test_line_below_threshold_fails(tmp_path, capsys):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 94,
            "num_statements": 100,
            "covered_branches": 100,
            "num_branches": 100,
        },
    )

    assert main([report]) == 1
    assert "line" in capsys.readouterr().out


def test_branch_below_threshold_fails(tmp_path, capsys):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 100,
            "num_statements": 100,
            "covered_branches": 94,
            "num_branches": 100,
        },
    )

    assert main([report]) == 1
    assert "branch" in capsys.readouterr().out


def test_both_metrics_reported(tmp_path, capsys):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 96,
            "num_statements": 100,
            "covered_branches": 97,
            "num_branches": 100,
        },
    )

    assert main([report]) == 0
    out = capsys.readouterr().out
    assert "96.00%" in out
    assert "97.00%" in out


def test_threshold_override(tmp_path):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 94,
            "num_statements": 100,
            "covered_branches": 96,
            "num_branches": 100,
        },
    )

    assert main([report, "--threshold", "90"]) == 0


def test_missing_branch_data_fails(tmp_path, capsys):
    report = _write_report(tmp_path, {"covered_lines": 100, "num_statements": 100})

    assert main([report]) == 1
    assert "branch data" in capsys.readouterr().out


def test_zero_branches_count_as_fully_covered(tmp_path):
    report = _write_report(
        tmp_path,
        {
            "covered_lines": 96,
            "num_statements": 100,
            "covered_branches": 0,
            "num_branches": 0,
        },
    )

    assert main([report]) == 0


def test_missing_report_fails(tmp_path, capsys):
    assert main([str(tmp_path / "nope.json")]) == 1
    assert "cannot read" in capsys.readouterr().out


def test_malformed_report_fails(tmp_path, capsys):
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {}}))

    assert main([str(report)]) == 1
    assert "does not look like a coverage.py JSON report" in capsys.readouterr().out
