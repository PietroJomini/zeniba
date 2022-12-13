import json
from typing import Dict, List, Optional

import requests

from zeniba.config import config
from zeniba.utils import cache


class AuthenticationError(Exception):
    """Failed login exception"""


def login(email: str, password: str):
    """Attempt to login using user email and password"""

    res = requests.post(
        f"{config['net']['onion']['endpoints']['login']}/rpc.php",
        data=dict(
            email=email,
            password=password,
            action="login",
            gg_json_mode="1",
        ),
        proxies=config["net"]["onion"]["proxies"],
    )

    content = json.loads(res.text)

    successfull_request = res.status_code == 200
    errors: Optional[List[Dict[str, str]]] = (
        content["errors"] if len(content["errors"]) > 0 else None
    )

    userid: Optional[str] = res.cookies.get("remix_userid")
    userkey: Optional[str] = res.cookies.get("remix_userkey")

    return successfull_request, errors, (userid, userkey)


class Client:
    """Authenticated client"""

    def __init__(
        self,
        uid: Optional[str] = None,
        key: Optional[str] = None,
    ):
        self._session = None
        self.cache = cache.Cache()

        # TODO check if keys are valid if they are user-provided
        self.uid = uid or self.cache.get(config["cache"]["uid"])
        self.key = key or self.cache.get(config["cache"]["key"])

    @property
    def session(self):

        if self._session is not None:
            return self._session

        if not self.is_authenticated():
            raise AuthenticationError("Keys needed")

        self._session = requests.Session()
        self._session.cookies["remix_userkey"] = self.key
        self._session.cookies["remix_userid"] = self.uid
        self._session.proxies = config["net"]["onion"]["proxies"]
        return self._session

    def is_authenticated(self):
        """Check if the user is authenticated"""

        return self.uid is not None and self.key is not None

    def login(self, email: str, password: str, force: bool = False):
        """Retrieve keys using email and password"""

        if self.is_authenticated() and not force:
            return self

        ok, errors, (uid, key) = login(email, password)

        if not ok or len(errors or []) > 0:
            raise AuthenticationError("Failed login", errors)

        self.uid = uid
        self.key = key

        self.cache.set(config["cache"]["uid"], str(uid))
        self.cache.set(config["cache"]["key"], str(key))

        return self

    def get(self, path: str, params: Optional[Dict] = None):
        """Get a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.get(
            f"{config['net']['onion']['endpoints']['main']}{path}",
            params=params or {},
            allow_redirects=True,
            headers=config["net"]["onion"]["headers"],
        )
