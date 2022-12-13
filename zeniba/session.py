from typing import Dict
import requests

from zeniba.config import config


class Protocol:
    """Base session"""

    def __init__(self, url: str, headers: Dict[str, str] | None = None):
        self.url = url
        self.headers = headers
        self.session = requests.Session()

    def get(self, path: str, params: Dict[str, str] | None = None):
        """Get a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.get(
            f"{self.url}{path}",
            params=params,
            allow_redirects=True,
            headers=self.headers,
        )

    def post(self, path: str, data: Dict[str, str]):
        """Post to a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.post(f"{self.url}{path}", headers=self.headers, data=data)


def onion(endpoint: str = "main"):
    """Construct a onion session"""

    protocol = Protocol(
        config["net"]["onion"]["endpoints"][endpoint],
        config["net"]["onion"]["headers"],
    )

    protocol.session.proxies = config["net"]["onion"]["proxies"]
    return protocol


def http(endpoint: str = "main"):
    """Construct a http session"""

    return Protocol(config["net"]["http"]["endpoints"][endpoint])
