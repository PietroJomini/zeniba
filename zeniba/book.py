from dataclasses import dataclass
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

    # TODO
    # description: List[str]


def book(client: Client, zid: str):
    """Book handler"""

    page = client.get(f"/book/{zid}").text
    parser = Parser(page)

    return Meta(
        title=parser.text_s('h1[itemprop="name"]'),
        authors=parser.text('a[itemprop="author"]'),
        cover=parser.get("div.z-book-cover > img", lambda tag: tag["src"])[0],
        categories=parser.property("categories"),
        volume=parser.property("volume", mod=int),
        year=parser.property("year", mod=int),
        edition=parser.property("edition"),
        publisher=parser.property("publisher"),
        language=parser.property("language"),
        pages=int(parser.property("pages")),
        isbn=parser.property(r"isbn.\31 3 + .property_isbn"),
        isbn_10=parser.property(r"isbn.\31 0"),
        isbn_13=parser.property(r"isbn.\31 3"),
        series=parser.property("series"),
    )
