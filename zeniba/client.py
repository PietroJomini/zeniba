from typing import Dict, Optional

import requests

import zeniba.config as config


class Client:
    def __init__(self, key: str, uid: str):
        self.session = requests.Session()
        self.session.cookies["remix_userkey"] = key
        self.session.cookies["remix_userid"] = uid
        self.session.proxies = config.PROXIES

    def get(self, path: str, params: Optional[Dict] = None):
        """Get a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.get(f"{config.URL}{path}", params=params or {})
