# Usage

**Table of contents**

- [Search](#search)
  - [Pagination](#pagination)
  - [Filters](#filters)
  - [Links](#links)
- [Book](#book)
  - [Download](#download)

## Search

To search books:

```python
pagination = client.search("a little life")
```

### Pagination

The result is paginated (like the website). `.read(n: int)` fetch, parse, cache and returns the `n`-th page of books:

```python
first_page = pagination.read(0)

# Here the items in the first page are cached,
# hence not parsed again but just included in the result
all_items = pagination.all()
```

To check the number of pages and books:

```python
pagination.total # number of pages
pagination.amount # number of items
pagination.exceds # boolean, True if the number of items is capped
```

### Filters

Zeniba support all the search filters supported by the website:

| filter               | key          | type                   | default      |
| -------------------- | ------------ | ---------------------- | ------------ |
| search query         | `query`      | `str`                  | **required** |
| match only if exact  | `exact`      | `bool`                 | `False`      |
| year range start     | `yearFrom`   | `Optional[int]`        | `None`       |
| year range end       | `yearTo`     | `Optional[int]`        | `None`       |
| languages            | `languages`  | `str[]`                | `[]`         |
| file extensions      | `extensions` | `str[]`                | `[]`         |
| result sorting order | `order`      | `config.params.orders` | `"popular"`  |

For example, to search some book written by the novelist Hanya Yanagihara in italian and french, and only in the `EPUB` format:

```python
client.search("Hanya Yanagihara", languages=["it", "fr"], extensions=["EPUB"])
```

Languages can be written both in short (`"en"`) and extended (`"english"`) format and are mapped with the same map used by the official client.

### Links

The pagination returns an array of `Links`, which are containers with the shape

```python
class Link:
    """Link to a given book"""

    # zlibrary id
    zid: str

    # index in the selected result order
    index: int

    # linked book meta
    title: str
    publisher: str
    authors: List[str]
    year: str
    language: str

    # small cover
    cover: str

    # downloadable file informations
    file_type: str
    file_size: str
```

## Book

Book detailed informations (the "book" dedicated page on the official client) can be fetched with

```python
book = client.book(link)
```

where `link` can be both a `zid` or a full `Link` returned from the search. The data is returned in a container similar to `Link`, but with more informations

```python
class Book:
    """Book meta"""

    # zlibrary id
    zid: str

    # download id
    did: str

    # bok detialed meta
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
```

### Download

To download a book

```python
name, content = client.download(book)
```

where `book` can be both a `Book` or a `zid` string. `name` is the original name of the file, and `content` is the `response.Content` in bytes.

To save the file various methods can be used, one of many being

```python
from pathlib import Path

# download the book
name, content = client.download(book)

# create a Path instance pointing to the folder where the
# file should be saved
file = Path(config.FOLDER) / name

# save the file
file.write_bytes(content)
```
