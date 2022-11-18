from typing import List, Optional
import requests

import zeniba.config as config
import zeniba.config.params as params


class Client:
    def __init__(self, key: str, uid: str):
        self.session = requests.Session()
        self.session.cookies["remix_userkey"] = key
        self.session.cookies["remix_userid"] = uid
        self.session.proxies = config.PROXIES

    def search(
        self,
        query: str,
        exact: bool = False,
        yearFrom: Optional[int] = None,
        yearTo: Optional[int] = None,
        languages: List[str] = [],
        extensions: List[str] = [],
        order: str = "popuar",
    ):
        """
        Simple search
        """

        # Params
        # - e=1 [exact match] (+ "" to the query)
        # - yearFrom={int}
        # - yearTo={int}
        # - languages[]={str}
        # - extensions[]={str}
        # - order={str}

        # When not in allowed lists, they fallback to defaults or are ignored.

        languages_extended = [
            params.languages_s.get(l) if params.languages_s.get(l) is not None else l
            for l in languages
        ]

        payload = {}
        payload["e"] = "1" if exact else None
        payload["yearFrom"] = yearFrom
        payload["yearTo"] = yearTo
        payload["languages[]"] = languages_extended
        payload["extensions[]"] = extensions
        payload["order"] = order

        query = f'"{query}"' if exact else query
        res = self.session.get(f"{config.URL}/s/{query}", params=payload)
        return res
