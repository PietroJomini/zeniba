import json
from pathlib import Path

import appdirs

from zeniba.config import config

DEFAULT_CACHE_PATH = appdirs.user_cache_dir(
    config["cache"]["appname"], config["cache"]["appauthor"]
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
        value = self.content.get(key)
        return value if value != "" else None

    def set(self, key: str, value: str | None):

        self.content[key] = value if value is not None else ""
        self.write()

    def clear(self):

        self.content = {}
        self.write()
