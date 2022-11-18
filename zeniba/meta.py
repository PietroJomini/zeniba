from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchResultItem:
    """Search result book"""

    index: int
    title: str
    publisher: str
    authors: List[str]
    year: str
    language: str
    file_type: str
    file_size: str


@dataclass
class SearchResult:
    """Search result"""

    items: List[SearchResultItem] = field(repr=False)
    pages: int
    page: int
    amount: int
    amount_exceeds: bool
