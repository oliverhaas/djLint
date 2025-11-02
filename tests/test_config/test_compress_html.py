"""Test for HTML compression and no_compression functionality.

Tests the compress_html formatter stage and the no_compression config option.

uv run pytest tests/test_config/test_compress_html.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    # Basic compression tests - multiline attributes get compressed by default
    pytest.param(
        ('<div class="foo\n           bar\n           baz"></div>'),
        ('<div class="foo bar baz"></div>\n'),
        ({}),
        id="basic_multiline_attribute_compression",
    ),
    # Multiple attributes compression
    pytest.param(
        (
            '<div class="foo\n'
            '           bar"\n'
            '     id="my\n'
            '         element"></div>'
        ),
        ('<div class="foo bar" id="my element"></div>\n'),
        ({}),
        id="multiple_multiline_attributes_compression",
    ),
    # The core test - JS comment preservation
    # Without JS formatting: comment gets flattened, breaking JS
    pytest.param(
        ('<div onclick="func(); // comment\nnextFunc();">Test</div>'),
        ('<div onclick="func(); // comment nextFunc();">Test</div>\n'),
        ({"format_attribute_js_json": False}),
        id="js_comment_flattened_without_js_formatting",
    ),
    # With JS formatting: comment structure preserved
    pytest.param(
        ('<div onclick="func(); // comment\nnextFunc();">Test</div>'),
        ('<div onclick="func(); // comment\n    nextFunc();">Test</div>\n'),
        ({"format_attribute_js_json": True}),
        id="js_comment_preserved_with_js_formatting",
    ),
    # Regular attributes still compress with JS formatting enabled
    pytest.param(
        ('<div class="foo\n           bar"></div>'),
        ('<div class="foo bar"></div>\n'),
        ({"format_attribute_js_json": True}),
        id="regular_attributes_still_compress_with_js_enabled",
    ),
    # Multiple attributes: entire tag skipped when JS attributes present
    pytest.param(
        (
            '<div onclick="func(); // comment\n'
            'nextFunc();" class="foo\n'
            'bar">Test</div>'
        ),
        (
            '<div onclick="func(); // comment\n'
            '    nextFunc();" class="foo\n'
            '    bar">Test</div>\n'
        ),
        ({"format_attribute_js_json": True}),
        id="mixed_js_and_regular_attributes",
    ),
    # HTMX attributes are also JS - should be preserved
    pytest.param(
        (
            "<div hx-on:click=\"console.log('test'); // comment\n"
            'doSomething();">Click</div>'
        ),
        (
            "<div hx-on:click=\"console.log('test'); // comment\n"
            '    doSomething();">Click</div>\n'
        ),
        ({"format_attribute_js_json": True}),
        id="htmx_js_comments_preserved",
    ),
    # Self-closing tags - regular attributes compressed
    pytest.param(
        (
            '<img src="image.jpg"\n'
            '     alt="description"\n'
            '     class="image responsive" />'
        ),
        (
            '<img src="image.jpg" alt="description" '
            'class="image responsive" />\n'
        ),
        ({}),
        id="self_closing_tag_attribute_compression",
    ),
    # Current tag-level behavior: entire tag preserved when JS attr present
    pytest.param(
        (
            '<div onclick="func(); // JS comment\n'
            'nextFunc();"\n'
            '     title="This is a very\n'
            "            long title\n"
            '            text">Content</div>'
        ),
        (
            '<div onclick="func(); // JS comment\n'
            '    nextFunc();"\n'
            '    title="This is a very\n'
            "    long title\n"
            '    text">Content</div>\n'
        ),
        ({"format_attribute_js_json": True}),
        id="tag_level_compression_entire_tag_preserved_when_js_present",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)
    printer(expected, source, output)
    assert expected == output
