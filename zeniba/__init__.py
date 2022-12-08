"""
Zeniba: a z-library scraper
"""


from typing import List, Optional, Union

from zeniba.book import Book, book, download
from zeniba.client import Client, login
from zeniba.search import Link, search


class Zeniba:
    """Zeniba entry point"""

    @staticmethod
    def login(email: str, password: str):
        _, _, (userid, userkey) = login(email, password)

        # TODO better error handling
        return Zeniba(str(userid), str(userkey))

    def __init__(self, uid: str, key: str):
        self.client = Client(key, uid)

    def book(self, link: Union[Link, str]):
        zid = link.zid if isinstance(link, Link) else link
        return book(self.client, zid)

    def download(self, book: Union[Book, str]):
        did = book.did if isinstance(book, Book) else book
        return download(self.client, did)

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
            self.client,
            query,
            exact,
            yearFrom,
            yearTo,
            languages,
            extensions,
            order,
        )
