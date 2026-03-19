from typer.testing import CliRunner

from triggermind.main import app


def test_cli_start_and_list(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TRIGGERMIND_DATA_DIR", str(tmp_path))
    runner = CliRunner()

    start = runner.invoke(app, ["start", "10m", "--message", "Write now"])
    assert start.exit_code == 0
    assert "Scheduled" in start.stdout

    listing = runner.invoke(app, ["list"])
    assert listing.exit_code == 0
    assert "Write now" in listing.stdout


def test_cli_cancel_unknown(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TRIGGERMIND_DATA_DIR", str(tmp_path))
    runner = CliRunner()

    result = runner.invoke(app, ["cancel", "missing-id"])
    assert result.exit_code != 0


def test_cli_guide_timer_flow(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TRIGGERMIND_DATA_DIR", str(tmp_path))
    runner = CliRunner()

    guided = runner.invoke(app, ["guide"], input="1\n5m\nStretch break\n")
    assert guided.exit_code == 0
    assert "Scheduled" in guided.stdout


def test_cli_update_message() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    assert "pip install -U triggermind" in result.stdout


def test_cli_ui_command(monkeypatch) -> None:
    runner = CliRunner()
    called = {"opened": False}

    def fake_ui() -> None:
        called["opened"] = True

    monkeypatch.setattr("triggermind.main.launch_ui", fake_ui)
    result = runner.invoke(app, ["ui"])
    assert result.exit_code == 0
    assert called["opened"] is True
