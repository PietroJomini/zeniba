import re
from dataclasses import InitVar, dataclass, field
from functools import lru_cache
from typing import List, Optional

from zeniba.client import Client
from zeniba.config.params import languages_s
from zeniba.parser import Parser as P


@dataclass
class Filters:
    """Search filters"""

    exact: bool = False
    yearFrom: Optional[int] = None
    yearTo: Optional[int] = None
    languages: List[str] = field(default_factory=list)
    extensions: List[str] = field(default_factory=list)
    order: str = "popular"
    page: int = 1

    def payload(self):
        _languages_ext = [
            languages_s.get(key) if languages_s.get(key) is not None else key
            for key in self.languages
        ]

        payload = {}
        payload["e"] = "1" if self.exact else None
        payload["yearFrom"] = self.yearFrom
        payload["yearTo"] = self.yearTo
        payload["languages[]"] = _languages_ext
        payload["extensions[]"] = self.extensions
        payload["order"] = self.order
        payload["page"] = self.page
        return payload


@dataclass
class Link:
    """Link to book"""

    index: int
    title: str
    publisher: str
    authors: List[str]
    year: str
    language: str

    file: InitVar[str]  # Only used on creation to slim the parsing block
    file_type: str = field(init=False)
    file_size: str = field(init=False)

    def __post_init__(self, file: str):
        ftype, fsize = file.split(",")
        self.file_type = ftype.strip()
        self.file_size = fsize.strip()


class Parser(P):
    """Search parser"""

    def paging(self):
        """Parse paging meta"""

        total_match = self.re(r"pagesTotal: (\d+)")
        current_match = self.re(r"pageCurrent: (\d+)")
        total = int(total_match.group(1)) if total_match is not None else 1
        current = int(current_match.group(1)) if current_match is not None else 1
        return total, current

    def amount(self):
        """Parse amount of links"""

        label = self.text_s("li.active > .totalCounter")
        groups = re.match(r"\((\d*)(\+)?\)", label)
        amount = int(groups.group(1)) if groups is not None else -1
        exceeds = groups is not None and groups.group(2) is not None
        return amount, exceeds

    def data(self):
        """Parse search data"""

        return [
            Link(
                index=int(item.text_s(".counter")),
                title=item.text_s("a[href*=book]:not(:has(img))"),
                publisher=item.text_s('a[title="Publisher"]'),
                authors=item.text(".authors > a"),
                year=item.property("year"),
                language=item.property("language"),
                file=item.text_s(".property__file > .property_value"),
            )
            for item in self.get(".resItemBox", lambda tag: P(str(tag)))
        ]


class Paging:
    """Paging handler"""

    def __init__(
        self,
        client: Client,
        path: str,
        filters: Optional[Filters] = None,
    ):
        self.client = client
        self.path = path
        self.filters = filters or Filters()
        self.total, _ = self.parser().paging()
        self.amount, self.exceeds = self.parser().amount()

    @lru_cache
    def parser(self, index: Optional[int] = None):
        """Retrieve indexed page and build parser"""

        self.filters.page = index or self.filters.page
        page = self.client.get(self.path, self.filters.payload())
        return Parser(page.text)

    def read(self, index: Optional[int] = None):
        """Read content of indexed or current page"""

        return self.parser(index).data()

    def all(self):
        """Read content from all pages"""

        link = []
        for index in range(self.total):
            link += self.read(index + 1)

        return link


def search(
    client: Client,
    query: str,
    exact: bool = False,
    yearFrom: Optional[int] = None,
    yearTo: Optional[int] = None,
    languages: List[str] = [],
    extensions: List[str] = [],
    order: str = "popuar",
):
    """Search handler"""

    path = f"/s/{query}"
    filters = Filters(exact, yearFrom, yearTo, languages, extensions, order)
    return Paging(client, path, filters)
