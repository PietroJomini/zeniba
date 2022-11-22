<p align="center">
  <!-- <img src="https://raw.githubusercontent.com/PietroJomini/zeniba/master/docs/logo.jpg" alt="zeniba"/> -->
  <img src="docs/logo.jpg" alt="zeniba" height="236"/>
</p>

<h1 align="center">zeniba</h1>
<p align="center"><i>"No-Face, why don't you stay with me?"</i></p>

<br>

### Examples

```python

from zeniba.client import Client

client = Client(config.KEY, config.UID)
pagination = client.search("sanderson", languages=["en", "it"], extensions=["EPUB"])

page = pagination.page(1)
meta = page.items[1]
title = meta.title # The Mistborn Trilogy [...]
author = meta.authors[0] # Brandon Sanderson
publisher = meta.publisher # TOR Books

everything = pagination.all()
```

```python
from zeniba import Zeniba

# API entry point.
# Open a connection to z-lib over the tor proxy
client = Zeniba(config.KEY, config.UID)

# Paginated search
pagination = client.search("sanderson", languages=["en", "it"], extensions=["EPUB"])
page = pagination.read(2)
link = page[0]

# Search result item.
# For a full list of fields see the documentation (TODO)
link.title # Mistborn: The Final Empire
link.publisher # Tor Teen
link.authors # ['Brandon Sanderson'],

# Book detailed page
book = client.book(link.zid)
book.isbn_10 # 0765377136
book.categories # Science Fiction & Fantasy
```
