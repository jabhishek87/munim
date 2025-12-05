"""Tests for base parser module."""
import pytest
from parser.base import BaseParser


class TestBaseParser:
    """Test cases for BaseParser class."""

    def test_normalize_date_ddmmyyyy(self):
        """Test date normalization with DD-MM-YYYY format."""
        parser = BaseParser(bank="Test", file_starts_with="test_")
        result = parser.normalize_date("15-03-2024")
        assert result == "2024-03-15"

    def test_normalize_date_ddmmyyyy_slash(self):
        """Test date normalization with DD/MM/YYYY format."""
        parser = BaseParser(bank="Test", file_starts_with="test_")
        result = parser.normalize_date("15/03/2024")
        assert result == "2024-03-15"

    def test_normalize_date_invalid(self):
        """Test date normalization with invalid format."""
        parser = BaseParser(bank="Test", file_starts_with="test_")
        with pytest.raises(ValueError):
            parser.normalize_date("invalid-date")

    def test_categorize_transactions_uncategorized(self):
        """Test transaction categorization with no matching keywords."""
        parser = BaseParser(bank="Test", file_starts_with="test_")
        result = parser.categorize_transactions("Unknown transaction")
        assert result == "uncategorized"

    def test_load_expenses_mappers(self):
        """Test loading expense mappers."""
        parser = BaseParser(bank="Test", file_starts_with="test_")
        result = parser.load_expenses_mappers()
        assert isinstance(result, dict)
