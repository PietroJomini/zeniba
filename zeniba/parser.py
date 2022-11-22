import re
from collections.abc import Callable
from typing import Any, Match, Pattern, Union

from bs4 import BeautifulSoup, Tag


class Parser:
    """Page parser"""

    def __init__(self, src: str):
        self.soup = BeautifulSoup(src, "html.parser")
        self.src = src

    def get(self, key: str, mod: Callable[[Tag], Any] = lambda tag: tag):
        tags = self.soup.select(key)
        items = [mod(tag) for tag in tags]
        return items

    def text(self, key: str):
        return self.get(key, lambda tag: tag.text.strip())

    def text_s(self, key: str, default: str = ""):
        items = self.text(key)
        return items[0] if len(items) > 0 else default

    def property(
        self,
        name: str,
        mod: Callable[[str], Any] = lambda value: value,
        default: str = "",
    ):
        """Common z-lib property structure getter"""

        tags = self.get(f"div.property_{name} > div.property_value")
        tag = tags[0] if len(tags) > 0 else default
        while isinstance(tag, Tag) and len(tag.find_all()) != 0:
            tag = tag.find()

        return mod(tag.text if isinstance(tag, Tag) else tag)

    def re(self, exp: Union[Pattern, str]):
        return re.search(exp, self.src)
