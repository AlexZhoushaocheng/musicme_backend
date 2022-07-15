import requests


def download(url_) -> bytes:
    res = requests.get(url=url_)
    return res.content
