"""
Zeniba: a z-library scraper
"""


from typing import List, Optional

from zeniba.book import book
from zeniba.client import Client
from zeniba.search import search


class Zeniba:
    """Zeniba entry point"""

    def __init__(self, key: str, uid: str):
        self.client = Client(key, uid)

    def book(self, zid: str):
        return book(self.client, zid)

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
