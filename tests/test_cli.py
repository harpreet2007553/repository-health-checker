import json

from repo_health_checker.cli import main


def test_main_lists_missing_items(monkeypatch, tmp_path, capsys):
    (tmp_path / "README.md").touch()
    (tmp_path / ".gitignore").touch()
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()

    monkeypatch.setattr("builtins.input", lambda _: str(tmp_path))

    exit_code = main()

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Missing items:" in output
    assert "LICENSE" in output
    assert "Health score:" in output


def test_main_shows_success_when_all_checks_pass(
    monkeypatch, tmp_path, capsys
):
    (tmp_path / "README.md").touch()
    (tmp_path / "LICENSE").touch()
    (tmp_path / ".gitignore").touch()
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_example.py").touch()

    monkeypatch.setattr("builtins.input", lambda _: str(tmp_path))

    exit_code = main()

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Great job! All checks passed." in output
    assert "Health score: 100%" in output


def test_main_accepts_path_argument(tmp_path, capsys):
    (tmp_path / "README.md").touch()
    (tmp_path / "LICENSE").touch()
    (tmp_path / ".gitignore").touch()
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_example.py").touch()

    exit_code = main([str(tmp_path)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Great job! All checks passed." in output


def test_main_outputs_json(tmp_path, capsys):
    (tmp_path / "README.md").touch()

    exit_code = main([str(tmp_path), "--json"])

    captured = capsys.readouterr().out
    data = json.loads(captured)

    assert exit_code == 0
    assert data["results"]["README.md"] is True
    assert data["results"]["LICENSE"] is False
    assert "LICENSE" in data["missing"]
    assert data["score"] == 20.0


def test_main_handles_nonexistent_directory(capsys):
    exit_code = main(["/nonexistent/path/for/sure"])

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: That folder does not exist." in output


def test_main_fail_under_threshold(tmp_path):
    (tmp_path / "README.md").touch()

    # Score is 20%, threshold is 80% -> should return 1
    exit_code = main([str(tmp_path), "--fail-under", "80"])
    assert exit_code == 1

    # Score is 20%, threshold is 20% -> should return 0
    exit_code_pass = main([str(tmp_path), "--fail-under", "20"])
    assert exit_code_pass == 0
