<p align="center">
  <!-- <img src="https://raw.githubusercontent.com/PietroJomini/zeniba/master/resources/logo.jpg" alt="zeniba"/> -->
  <img src="resources/logo.jpg" alt="zeniba" height="236"/>
</p>

<h1 align="center">zeniba</h1>
<p align="center"><i>"No-Face, why don't you stay with me?"</i></p>

<br>

### Quick example

```python
from zeniba import Zeniba

client = Zeniba().login(config.EMAIL, config.PASSWORD)
links = client.search("a little life").read(0)
book = client.book(links[0])

name, content = client.download(book)
```

### Not so quick example

[docs](docs/index.md)
