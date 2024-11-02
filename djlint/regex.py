# Call this module something like `regex.py` or `regex_custom_wrappers.py` 

import re
from functools import lru_cache


def search(regex, text, use_cache: bool = True, flags=None, **kwargs):
    if use_cache:
        re_compiled = _compile_cached(regex, flags=flags)
        return re_compiled.search(text, **kwargs)
    return re.search(regex, text, flags=flags, **kwargs)

# ... more regex functions


def finditer(regex, text, use_cache: bool = True, flags=None, **kwargs):
    if use_cache:
        re_compiled = _compile_cached(regex, flags=flags)
        return re_compiled.finditer(text, **kwargs)
    return re.finditer(regex, text, flags=flags, **kwargs)


def match(regex, text, use_cache: bool = True, flags=None, **kwargs):
    if use_cache:
        re_compiled = _compile_cached(regex, flags=flags)
        return re_compiled.match(text, **kwargs)
    return re.match(regex, text, flags=flags, **kwargs)


def sub(regex, repl, text, use_cache: bool = True, flags=None, **kwargs):
    if use_cache:
        re_compiled = _compile_cached(regex, flags=flags)
        return re_compiled.sub(repl, text, **kwargs)
    return re.sub(regex, repl, text, flags=flags, **kwargs)

@lru_cache(maxsize=256)
def _compile_cached(regex, flags=None) -> re.Pattern:
    return re.compile(regex, flags=flags)