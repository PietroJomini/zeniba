import json
from typing import Dict, List, Optional

from zeniba.config import config
from zeniba.utils import cache
from zeniba.session import onion, Protocol, http


class AuthenticationError(Exception):
    """Failed login exception"""


def login(email: str, password: str, session: Protocol):
    """Attempt to login using user email and password"""

    data = dict(email=email, password=password, action="login", gg_json_mode="1")
    res = session.post("rpc.php", data=data)

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
        self._session = onion()
        self.cache = cache.Cache()

        # TODO check if keys are valid if they are user-provided
        self.uid = uid or self.cache.get(config["cache"]["uid"])
        self.key = key or self.cache.get(config["cache"]["key"])

    @property
    def session(self):

        if not self.is_authenticated():
            raise AuthenticationError("Keys needed")

        self._session.session.cookies["remix_userkey"] = self.key
        self._session.session.cookies["remix_userid"] = self.uid
        return self._session

    def is_authenticated(self):
        """Check if the user is authenticated"""

        return self.uid is not None and self.key is not None

    def login(
        self, email: str, password: str, force: bool = False, use_onion: bool = False
    ):
        """Retrieve keys using email and password"""

        if self.is_authenticated() and not force:
            return self

        login_session = onion("login") if use_onion else http("login")
        ok, errors, (uid, key) = login(email, password, login_session)

        if not ok or len(errors or []) > 0:
            raise AuthenticationError("Failed login", errors)

        self.uid = uid
        self.key = key

        self.cache.set(config["cache"]["uid"], str(uid))
        self.cache.set(config["cache"]["key"], str(key))

        return self

    def logout(self):
        """Delete session keys"""

        self.uid = None
        self.key = None
        self.cache.set(config["cache"]["uid"], None)
        self.cache.set(config["cache"]["key"], None)

    def get(self, path: str, params: Dict[str, str] | None = None):
        """Get a page"""

        return self.session.get(path, params)
