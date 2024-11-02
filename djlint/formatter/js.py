"""djLint function to call jsbeautifier."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import jsbeautifier
import re
from jsbeautifier.javascript.options import BeautifierOptions

from ..helpers import RE_FLAGS_IS, child_of_unformatted_block

if TYPE_CHECKING:
    from ..settings import Config


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""

    def launch_formatter(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Add break after if not in ignored block."""
        if child_of_unformatted_block(config, html, match):
            return match.group()

        if not match.group(3).strip():
            return match.group()

        indent = len(match.group(1)) * " "

        # because of the param options for js-beautifier we cannot pass
        # in a fixed space leading.
        # so, call formatter twice, once with a fake indent.
        # check which lines changed (these are the formattable lines)
        # and add the leading space to them.

        config.js_config["indent_level"] = 1
        opts = BeautifierOptions(config.js_config)
        beautified_lines = jsbeautifier.beautify(
            match.group(3), opts
        ).splitlines()

        config.js_config["indent_level"] = 2
        opts = BeautifierOptions(config.js_config)
        beautified_lines_test = jsbeautifier.beautify(
            match.group(3), opts
        ).splitlines()

        beautified = ""
        for line, test in zip(beautified_lines, beautified_lines_test):
            beautified += "\n"
            if line == test:
                beautified += line
                continue
            beautified += indent + line

        return match.group(1) + match.group(2) + beautified + "\n" + indent

    func = partial(launch_formatter, config, html)

    return re.sub(
        r"([ ]*?)(<(?:script)\b(?:\"[^\"]*\"|'[^']*'|{[^}]*}|[^'\">{}])*>)(.*?)(?=</script>)",
        func,
        html,
        flags=RE_FLAGS_IS,
    )
