"""Test for JS/JSON attribute formatting.

--format-js-attributes
--js-attribute-pattern

uv run pytest tests/test_config/test_format_js_json_attributes.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        ('<div data-config=\'{"name": "value"}\'></div>'),
        ('<div data-config=\'{"name": "value"}\'></div>\n'),
        ({"format_attribute_js_json": True, "max_attribute_length": 0}),
        id="json_single_property_no_formatting",
    ),
    pytest.param(
        ('<div data-config=\'{"name": "value", "enabled": true}\'></div>'),
        (
            "<div data-config='{\n"
            '                    "name": "value",\n'
            '                    "enabled": true\n'
            "                  }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="json_two_properties_multiline_medium_attr",
    ),
    pytest.param(
        ('<div data-x=\'{"name": "value", "enabled": true}\'></div>'),
        (
            "<div data-x='{\n"
            '               "name": "value",\n'
            '               "enabled": true\n'
            "             }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="json_two_properties_multiline_short_attr",
    ),
    pytest.param(
        (
            '<div data-very-long-attribute-name=\'{"name": "value", "enabled": true}\'></div>'
        ),
        (
            "<div data-very-long-attribute-name='{\n"
            '                                      "name": "value",\n'
            '                                      "enabled": true\n'
            "                                    }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="json_two_properties_multiline_long_attr",
    ),
    pytest.param(
        ("<div onclick='{action: \"click\"}'></div>"),
        ("<div onclick='{action: \"click\"}'></div>\n"),
        ({"format_attribute_js_json": True, "max_attribute_length": 0}),
        id="js_single_property_no_formatting",
    ),
    pytest.param(
        ("<div onclick='{action: \"click\", preventDefault: true}'></div>"),
        (
            "<div onclick='{\n"
            '                action: "click",\n'
            "                preventDefault: true\n"
            "              }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_two_properties_multiline",
    ),
    pytest.param(
        ("<div onclick='foo();'></div>"),
        ("<div onclick='foo();'></div>\n"),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_code_single_function_no_formatting",
    ),
    pytest.param(
        ("<div onclick='foo(); var x = 1; baz();'></div>"),
        (
            "<div onclick='foo();\n"
            "              var x = 1;\n"
            "              baz();'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_code_multiple_statements_multiline",
    ),
    pytest.param(
        ("<div onclick='foo(); baz();'></div>"),
        ("<div onclick='foo(); baz();'></div>\n"),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 50,
            "indent_js": 2,
        }),
        id="js_code_under_max_length_no_formatting",
    ),
    pytest.param(
        (
            "<div class='foo-baz'></div>"
            "<div id='my-element-id'></div>"
            "<input name='user-name' />"
            "<div title='Page Title'></div>"
            "<input type='text' />"
            "<input value='some-value' />"
            "<div role='button'></div>"
            "<div aria-label='Close Button'></div>"
            "<a href='/path/to/page'></a>"
            "<img src='/path/to/image.jpg' />"
            "<img alt='Image Description' />"
        ),
        (
            "<div class='foo-baz'></div>\n"
            "<div id='my-element-id'></div>\n"
            "<input name='user-name' />\n"
            "<div title='Page Title'></div>\n"
            "<input type='text' />\n"
            "<input value='some-value' />\n"
            "<div role='button'></div>\n"
            "<div aria-label='Close Button'></div>\n"
            "<a href='/path/to/page'></a>\n"
            "<img src='/path/to/image.jpg' />\n"
            "<img alt='Image Description' />\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="non_js_attributes_no_formatting",
    ),
    pytest.param(
        (
            "<div onclick='{foo: \"bar\", get baz() { return this.foo; }}'></div>"
        ),
        (
            "<div onclick='{\n"
            '                 foo: "bar",\n'
            "                 get baz() {\n"
            "                    return this.foo;\n"
            "                 }\n"
            "              }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 3,
        }),
        id="js_getter_function_nested_indent",
    ),
    pytest.param(
        # Test default indent_js behavior (no indent_js specified)
        ('<div onclick=\'{"foo": "bar", "baz": "qux"}\'></div>'),
        (
            "<div onclick='{\n"
            '                  "foo": "bar",\n'
            '                  "baz": "qux"\n'
            "              }'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            # Note: no indent_js specified, should use default
        }),
        id="js_object_default_indent",
    ),
    pytest.param(
        ('<div data-id="{{ input }}"></div>'),
        ('<div data-id="{{ input }}"></div>\n'),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="template_tag_no_formatting",
    ),
    pytest.param(
        (
            "<div data-config='{% if user %}"
            '{"active": true}{% endif %}\'></div>'
        ),
        (
            '<div data-config=\'{% if user %}{"active": true}\n'
            "{% endif %}\n"
            "'></div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="jinja_template_tag_with_json_no_js_formatting",
    ),
    pytest.param(
        (
            '<div data-config="{{ config.json }}" '
            'onclick=\'{"action": "click"}\'></div>'
        ),
        (
            '<div data-config="{{ config.json }}"\n'
            '     onclick=\'{"action": "click"}\'></div>\n'
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="mixed_template_and_js_no_formatting_when_template_present",
    ),
    pytest.param(
        (
            '<div hx-on:click="document.getElementById('
            "'{{ widget_id }}').value = this.dataset.id; "
            "document.getElementById('{{ widget_id }}_display')"
            ".value = this.textContent.trim(); "
            "this.parentElement.innerHTML = '';\">"
            "</div>"
        ),
        (
            "<div hx-on:click=\"document.getElementById('{{ widget_id }}').value = this.dataset.id;\n"
            "                  document.getElementById('{{ widget_id }}_display').value = this.textContent.trim();\n"
            "                  this.parentElement.innerHTML = '';\">"
            "</div>\n"
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_with_template_tokens_formatted_but_templates_preserved",
    ),
    pytest.param(
        ('<div hx-on:click="foo.bar(); baz.qux();"></div>'),
        (
            '<div hx-on:click="foo.bar();\n'
            '                  baz.qux();"></div>\n'
        ),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_continuation_line_indentation",
    ),
    pytest.param(
        ('<div onclick="func();\nnextFunc();">Test</div>'),
        ('<div onclick="func();\n    nextFunc();">Test</div>\n'),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_newline_without_comment_preserves_newline",
    ),
    pytest.param(
        ('<div onclick="func(); // comment\nnextFunc();">Test</div>'),
        ('<div onclick="func(); // comment\n    nextFunc();">Test</div>\n'),
        ({
            "format_attribute_js_json": True,
            "max_attribute_length": 0,
            "indent_js": 2,
        }),
        id="js_comment_followed_by_code_preserves_newline",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)
    printer(expected, source, output)
    assert expected == output
