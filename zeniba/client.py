import requests

import zeniba.config as config


class Client:
    def __init__(self, key: str, uid: str):
        self.session = requests.Session()
        self.session.cookies["remix_userkey"] = key
        self.session.cookies["remix_userid"] = uid
        self.session.proxies = config.PROXIES

    def search(self, query: str):
        """Simple search"""

        res = self.session.get(f"{config.URL}/s/{query}")
        return res
