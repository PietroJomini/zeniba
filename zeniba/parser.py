from bs4 import BeautifulSoup
from zeniba.meta import SearchResult, SearchResultItem
import re


class Parser:
    def __init__(self, src: str):
        self.src = src
        self.soup = BeautifulSoup(src, "html.parser")


class Search(Parser):
    def parse(self) -> SearchResult:

        pages_match = re.search(r"pagesTotal: (\d+)", self.src)
        page_match = re.search(r"pageCurrent: (\d+)", self.src)
        pages = int(pages_match.group(1) if pages_match is not None else 1)
        page = int(page_match.group(1) if page_match is not None else 1)

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
                SearchResultItem(
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
        amount_e = groups is not None and groups.group(2) is not None

        return SearchResult(
            items=books, pages=pages, page=page, amount=amount, amount_exceeds=amount_e
        )
