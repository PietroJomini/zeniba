from bs4 import BeautifulSoup


class Parser:
    def __init__(self, src: str):
        self.src = src
        self.soup = BeautifulSoup(src, "html.parser")
