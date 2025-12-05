"""Tests for CLI module."""
from click.testing import CliRunner
from cli import cli


class TestCLI:
    """Test cases for CLI commands."""

    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Munim" in result.output

    def test_parse_help(self):
        """Test parse command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["parse", "--help"])
        assert result.exit_code == 0
        assert "Parse bank statements" in result.output

    def test_parse_all_help(self):
        """Test parse_all command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "parse-all" in result.output

    def test_verbose_option_exists(self):
        """Test that verbose option is available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "--verbose" in result.output or "-v" in result.output

    def test_log_file_option_exists(self):
        """Test that log-file option is available."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "--log-file" in result.output
