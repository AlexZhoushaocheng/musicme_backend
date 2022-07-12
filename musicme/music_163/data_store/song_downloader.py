
import requests

class SongDownloader:
    @classmethod
    def download(cls, url:str):
        res = requests.get(url=url)
        return res.content