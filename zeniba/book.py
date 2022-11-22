from dataclasses import dataclass
from functools import cached_property
from typing import List

from zeniba.client import Client
from zeniba.parser import Parser


@dataclass
class Meta:
    """Book meta"""

    title: str
    authors: List[str]
    cover: str
    categories: List[str]
    volume: int
    year: int
    edition: str
    publisher: str
    language: str
    pages: int
    isbn: str
    isbn_10: str
    isbn_13: str
    series: List[str]
    # description: List[str]


class Book:
    """Book handler"""

    def __init__(self, client: Client, zid: str):
        self.page = client.get(f"/book/{zid}").text
        self.parser = Parser(self.page)

    @cached_property
    def meta(self):
        """Get meta"""

        return Meta(
            title=self.parser.text_s('h1[itemprop="name"]'),
            authors=self.parser.text('a[itemprop="author"]'),
            cover=self.parser.get("div.z-book-cover > img", lambda tag: tag["src"])[0],
            categories=self.parser.property("categories"),
            volume=self.parser.property("volume", mod=int),
            year=self.parser.property("year", mod=int),
            edition=self.parser.property("edition"),
            publisher=self.parser.property("publisher"),
            language=self.parser.property("language"),
            pages=int(self.parser.property("pages")),
            isbn=self.parser.property(r"isbn.\31 3 + .property_isbn"),
            isbn_10=self.parser.property(r"isbn.\31 0"),
            isbn_13=self.parser.property(r"isbn.\31 3"),
            series=self.parser.property("series"),
        )
