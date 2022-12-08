from dataclasses import dataclass
from typing import List

from zeniba.client import Client
from zeniba.parser import Parser


@dataclass
class Book:
    """Book meta"""

    # ids
    zid: str
    did: str

    # meta
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

    def __post_init__(self):

        # adjust did (link -> did)
        self.did = self.did.replace("/dl/", "")


def download(client: Client, book: Book):
    """Book downloader"""

    res = client.get(f"/dl/{book.did}")

    # TODO check if the pattern of the header is always the same
    content_disposition = res.headers["Content-Disposition"]
    filename = content_disposition.split(";filename*=")[0].replace(
        "attachment; filename=", ""
    )[1:-1]

    return filename, res.content


def book(client: Client, zid: str):
    """Book handler"""

    page = client.get(f"/book/{zid}").text
    parser = Parser(page)

    return Book(
        zid=zid,
        did=parser.field("a.dlButton", "href")[0],
        title=parser.text_s('h1[itemprop="name"]'),
        authors=parser.text('a[itemprop="author"]'),
        cover=parser.field("div.z-book-cover > img", "src")[0],
        categories=parser.property("categories"),
        volume=parser.property("volume", mod=int, default="-1"),
        year=parser.property("year", mod=int, default="-1"),
        edition=parser.property("edition"),
        publisher=parser.property("publisher"),
        language=parser.property("language"),
        pages=parser.property("pages", mod=int, default="-1"),
        isbn=parser.property(r"isbn.\31 3 + .property_isbn"),
        isbn_10=parser.property(r"isbn.\31 0"),
        isbn_13=parser.property(r"isbn.\31 3"),
        series=parser.property("series"),
    )
