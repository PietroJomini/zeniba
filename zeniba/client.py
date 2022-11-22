import json
from typing import Dict, List, Optional

import requests

import zeniba.config as config


def login(email: str, password: str):
    """Attempt to login using user email and password"""

    res = requests.post(
        f"{config.LOGIN_URL}/rpc.php",
        data=dict(
            email=email,
            password=password,
            action="login",
            gg_json_mode="1",
        ),
        proxies=config.PROXIES,
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
    def __init__(self, key: str, uid: str):
        self.session = requests.Session()
        self.session.cookies["remix_userkey"] = key
        self.session.cookies["remix_userid"] = uid
        self.session.proxies = config.PROXIES

    def get(self, path: str, params: Optional[Dict] = None):
        """Get a page"""

        path = path if path.startswith("/") else f"/{path}"
        return self.session.get(f"{config.URL}{path}", params=params or {})
