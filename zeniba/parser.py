from collections.abc import Callable
from typing import Any

from bs4 import BeautifulSoup, Tag


class Parser:
    def __init__(self, src: str):
        self.src = src
        self.soup = BeautifulSoup(src, "html.parser")

    def get(self, key: str, mod: Callable[[Tag], Any] = lambda tag: tag):
        tags = self.soup.select(key)
        items = [mod(tag) for tag in tags]
        return items

    def text(self, key: str):
        return self.get(key, lambda tag: tag.text.strip())

    def text_s(self, key: str):
        return self.text(key)[0]

    def property(
        self,
        name: str,
        mod: Callable[[str], Any] = lambda value: value,
    ):
        """Common z-lib property structure getter"""

        tag = self.get(f"div.property_{name} > div.property_value")[0]
        while isinstance(tag, Tag) and len(tag.find_all()) != 0:
            tag = tag.find()

        return mod(tag.text)
