"""
Zeniba: a z-library scraper
"""


from typing import List, Optional, Union

from zeniba.book import Book, book, download
from zeniba.client import Client
from zeniba.search import Link, search


class Zeniba(Client):
    """Zeniba client with shortucut to entities getters"""

    def book(self, link: Union[Link, str]):
        zid = link.zid if isinstance(link, Link) else link
        return book(self, zid)

    def download(self, book: Union[Book, str]):
        did = book.did if isinstance(book, Book) else book
        return download(self, did)

    def search(
        self,
        query: str,
        exact: bool = False,
        yearFrom: Optional[int] = None,
        yearTo: Optional[int] = None,
        languages: List[str] = [],
        extensions: List[str] = [],
        order: str = "popuar",
    ):
        return search(
            self, query, exact, yearFrom, yearTo, languages, extensions, order
        )
