"""Unit tests for file handling utilities."""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from utils.file_handling import strip_markdown


class TestStripMarkdown:
    """Tests for strip_markdown function."""

    def test_strip_simple_markdown(self):
        """Test stripping basic markdown formatting."""
        markdown_text = "**bold** and *italic* text"
        result = strip_markdown(markdown_text)
        assert "bold" in result
        assert "italic" in result
        assert "**" not in result
        assert "*" not in result

    def test_strip_headers(self):
        """Test stripping markdown headers."""
        markdown_text = "# Header 1\n## Header 2\n### Header 3\nContent"
        result = strip_markdown(markdown_text)
        assert "#" not in result
        assert "Header 1" in result
        assert "Header 2" in result
        assert "Header 3" in result

    def test_strip_links(self):
        """Test stripping markdown links."""
        markdown_text = "[Link text](https://example.com)"
        result = strip_markdown(markdown_text)
        assert "[" not in result
        assert "]" not in result
        assert "(" not in result
        assert ")" not in result
        assert "Link text" in result

    def test_strip_code_blocks(self):
        """Test stripping markdown code blocks."""
        markdown_text = "Some text\n```python\ncode here\n```\nMore text"
        result = strip_markdown(markdown_text)
        assert "```" not in result
        assert "Some text" in result
        assert "More text" in result

    def test_strip_unordered_lists(self):
        """Test stripping markdown lists."""
        markdown_text = "- Item 1\n- Item 2\n* Item 3\n* Item 4"
        result = strip_markdown(markdown_text)
        assert "-" not in result or "Item" in result
        assert "*" not in result or "Item" in result
        assert "Item 1" in result
        assert "Item 2" in result

    def test_empty_string(self):
        """Test stripping empty string."""
        result = strip_markdown("")
        assert result == ""

    def test_plain_text_unchanged(self):
        """Test that plain text without markdown is mostly unchanged."""
        plain_text = "This is plain text without any markdown formatting."
        result = strip_markdown(plain_text)
        assert "plain text" in result

    def test_complex_markdown(self):
        """Test stripping complex markdown with mixed elements."""
        markdown = """# Report Title

## Section 1
This is **bold text** with *italic* and ***bold italic***.

### Subsection
- Finding 1
- Finding 2

[Link](https://example.com)

```
code sample
```

Regular paragraph here."""
        result = strip_markdown(markdown)
        assert "Report Title" in result
        assert "Section 1" in result
        assert "#" not in result
        assert "**" not in result
        assert "[Link]" not in result or "Link" in result

    def test_preserve_text_content(self):
        """Test that actual text content is preserved."""
        markdown = "**Important**: Patient has symptoms. *Follow up* required."
        result = strip_markdown(markdown)
        assert "Important" in result
        assert "Patient" in result
        assert "symptoms" in result
        assert "Follow up" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
