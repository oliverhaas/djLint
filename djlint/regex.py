# Call this module something like `regex.py` or `regex_custom_wrappers.py` 

import re
from functools import lru_cache


def search(regex, text, use_cache: bool = True, flags=None, **kwargs):
    if use_cache:
        re_compiled = _compile_cached(regex, flags=flags)
        return re_compiled.search(text, **kwargs)
    return re.search(regex, text, flags=flags, **kwargs)

# ... more regex functions

@lru_cache(maxsize=256)
def _compile_cached(regex, flags=None) -> re.Pattern:
    return re.compile(regex, flags=flags)