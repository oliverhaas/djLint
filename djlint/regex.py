from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AnyStr, Callable

import re
from re import DOTALL, IGNORECASE, MULTILINE, VERBOSE, I, M, S, X  # noqa: F401


def search(
    pattern: str | re.Pattern[str],
    string: str,
    flags: int = 0,
    **kwargs: Any,
) -> re.Match[str] | None:
    return _compile_cached(pattern, flags=flags).search(string, **kwargs)


def finditer(
    pattern: str | re.Pattern[str],
    string: str,
    flags: int = 0,
    **kwargs: Any,
) -> re.Match[str]:
    return _compile_cached(pattern, flags=flags).finditer(string, **kwargs)


def match(
    pattern: str | re.Pattern[str],
    string: str,
    flags: int = 0,
    **kwargs: Any,
) -> re.Match[str] | None:
    return _compile_cached(pattern, flags=flags).match(string, **kwargs)


def sub(
    pattern: str | re.Pattern[str],
    repl: str | Callable[[re.Match[str]], str],
    string: str,
    flags: int = 0,
    **kwargs: Any,
) -> str:
    return _compile_cached(pattern, flags=flags).sub(repl, string, **kwargs)


@lru_cache(maxsize=256)
def _compile_cached(pattern: AnyStr | re.Pattern[AnyStr], flags: int = 0) -> re.Pattern[AnyStr]:
    return re.compile(pattern, flags=flags)
