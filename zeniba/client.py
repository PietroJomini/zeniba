from typing import Dict, List, Optional

import requests

import zeniba.config as config
from zeniba.search import Filters
from zeniba.search import Parser as Search
from zeniba.search import Result


class Client:
    def __init__(self, key: str, uid: str):
        self.session = requests.Session()
        self.session.cookies["remix_userkey"] = key
        self.session.cookies["remix_userid"] = uid
        self.session.proxies = config.PROXIES

    def get(self, path: str, params: Optional[Dict]):
        """Get a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.get(f"{config.URL}{path}", params=params or {})

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
        """Simple search"""

        path = f"/s/{query}"
        filters = Filters(exact, yearFrom, yearTo, languages, extensions, order)
        return Paging(self, path, filters)


class Paging:
    """Paging handler"""

    def __init__(self, client: Client, path: str, filters: Optional[Filters]):

        self.path = path
        self.client = client
        self.filters = filters or Filters()
        self.pages = {}

        res = client.get(self.path, self.filters.payload())
        parser = Search(res.text)
        page, amount = parser.paging()

        self.pages[page] = parser.data()
        self.amount = amount

    def page(self, index: int) -> Result:
        """Parse a page"""

        if index not in self.pages:
            self.filters.page = index
            res = self.client.get(self.path, self.filters.payload())
            self.pages[index] = Search(res.text).data()

        return self.pages[index]

    def all(self):
        """Fetch data from all pages"""

        partials = [self.page(i + 1) for i in range(self.amount)]

        return Result(
            items=[item for page in partials for item in page.items],
            amount=partials[0].amount,
            amount_exceeds=partials[0].amount_exceeds,
        )
