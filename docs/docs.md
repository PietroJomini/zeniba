# Zeniba docs

## API Front-end

### Session

With the new version of the website (see below @"TOR proxy") a session is required to surf the library. Zeniba implements a email-password login, that can be bypassed by giving directly the user `uid` and `key`.

#### `login`

Opening a session through a email-password login is as symple as writing a line of code:

```python
from zeniba import Zeniba

client = Zeniba.login(config.EMAIL, config.PASSWORD)
```

#### `uid`-`key` bypass

If for any reason providing directly the user `uid` and `key` is preferrable, doing so is as simple as

```python
from zeniba import Zeniba

client = Zeniba(config.UID, config.KEY)
```

The user `uid` and `key` can be found in the cookies of the website, for example by running `document.cookie` into the browser console, which should return a string containing

```
remix_userkey=USER_KEY; remix_userid=USER_ID;
```

This method is preferrable if it is required to open a big number of clients in short period of time, since zlibrary standard login can (and will) ban your ip for a short period of time if it receives too much requests.

### Search

To search books:

```python
pagination = client.search("a little life")
```

#### Pagination

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

#### Filters

Zeniba support all the search filters supported by the website:

| filter               | key          | type                   | default      |
| -------------------- | ------------ | ---------------------- | ------------ | ------ |
| search query         | `query`      | `str`                  | **required** |
| match only if exact  | `exact`      | `bool`                 | `False`      |
| year range start     | `yearFrom`   | `int                   | None`        | `None` |
| year range end       | `yearTo`     | `int                   | None`        | `None` |
| languages            | `languages`  | `str[]`                | `[]`         |
| file extensions      | `extensions` | `str[]`                | `[]`         |
| result sorting order | `order`      | `config.params.orders` | `"popular"`  |

For example, to search some book ofwritten by the novelist Hanya Yanagihara in italian and french, and only in the `EPUB` format:

```python
client.search("Hanya Yanagihara", languages=["it", "fr"], extensions=["EPUB"])
```

Languages can be written both in short (`"en"`) and extended (`"english"`) format and are mapped with the same map used by the official client.

#### Links

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

### Book

Book detailed informations (the "book" dedicated page on the official client) can be fetched with

```python
book = client.book(link)
```

where `link` can be both a `zid` or a full `Link` returned from the search. The data is returned in a container similat to `Link`, but with more informations

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

#### Download

To download a book

```python
name, content = client.download(book)
```

where `book` can be both a `Book` or a `zid` string. `name` is the original name of the file, and `content` is the `response.Content` in bytes.

To save the file various methods can be used, one of meny being

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

## Config

### TOR proxy

Since z-library domains have been seized by UPS, now the website is only accessible through tor. Installing / setting up the tor proxies is hence left as an exercise for the reader.

The only requirement as of Zeniba is to modify them if they differ from the default ones, which are:

```json
{
  "http": "socks5h://127.0.0.1:9150",
  "https": "socks5h://127.0.0.1:9150"
}
```

### Endpoints

The default onion endpoints are:

| key     | endpoint                                                               |
| ------- | ---------------------------------------------------------------------- |
| login   | http://loginzlib2vrak5zzpcocc3ouizykn6k5qecgj2tzlnab5wcbqhembyd.onion/ |
| lybrary | http://bookszlibb74ugqojhzhg2a63w5i2atv5bqarulgczawnbmsb6s6qead.onion3 |

They can be modified in `config/__init__.py`.
