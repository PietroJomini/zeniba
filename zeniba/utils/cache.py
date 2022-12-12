import json
from pathlib import Path

import appdirs

from zeniba import config

DEFAULT_CACHE_PATH = appdirs.user_cache_dir(
    config.CACHE["appname"], config.CACHE["appauthor"]
)


class Cache:
    """Cached dict"""

    def __init__(self, cachedir: str | Path = DEFAULT_CACHE_PATH):

        self.path = Path(cachedir)
        self.content = {}
        self.load()

    def load(self):
        """Ensure cache file exists"""

        if not self.path.exists():
            self.path.touch()

        try:
            self.read()
        except json.decoder.JSONDecodeError:
            self.write()

    def read(self):
        self.content = json.loads(self.path.read_text())

    def write(self):
        self.path.write_text(json.dumps(self.content))

    def get(self, key: str):

        self.read()
        return self.content.get(key)

    def set(self, key: str, value: str):

        self.content[key] = value
        self.write()

    def clear(self):

        self.content = {}
        self.write()
