import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

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
class Item:
    """Search result item"""

    index: int
    title: str
    publisher: str
    authors: List[str]
    year: str
    language: str
    file_type: str
    file_size: str


@dataclass
class Result:
    """Search result page"""

    items: List[Item] = field(repr=False)
    amount: int
    amount_exceeds: bool


class Parser(P):
    """Search result page parser"""

    def paging(self) -> Tuple[int, int]:
        """Parse paging data"""

        pages_match = re.search(r"pagesTotal: (\d+)", self.src)
        page_match = re.search(r"pageCurrent: (\d+)", self.src)
        pages = int(pages_match.group(1) if pages_match is not None else 1)
        page = int(page_match.group(1) if page_match is not None else 1)

        return page, pages

    def data(self) -> Result:

        books = []
        for item in self.soup.select(".resItemBox"):
            title = item.select_one("a[href*=book]:not(:has(img))")
            publisher = item.select_one("a[title=Publisher]")
            authors = item.select(".authors > a")
            year = item.select_one(".property_year > .property_value")
            language = item.select_one(".property_language > .property_value")
            index = item.select_one(".counter")

            file = item.select_one(".property__file > .property_value")
            file = (file.text if file is not None else ",").split(",")

            books.append(
                Item(
                    index=int(index.text if index is not None else -1),
                    title=title.text if title is not None else "",
                    publisher=publisher.text if publisher is not None else "",
                    authors=[author.text for author in authors],
                    year=year.text if year is not None else "",
                    language=language.text if language is not None else "",
                    file_type=file[0].strip(),
                    file_size=file[1].strip(),
                )
            )

        amount = self.soup.select_one("li.active > .totalCounter")
        groups = re.match(r"\((\d*)(\+?)\)", amount.text if amount is not None else "")
        amount = int(groups.group(1)) if groups is not None else -1
        amount_e = (
            groups is not None
            and groups.group(2) is not None
            and len(groups.group(2)) != 0
        )

        return Result(items=books, amount=amount, amount_exceeds=amount_e)
