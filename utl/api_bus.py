import urllib.request
from urllib.parse import quote
import json

class API(object):
    key: str
    url: str
    def __init__(self, key, url):
        self.key = key
        self.url = url
    
    def get_url(self, query="") -> str:
        query = quote(query)
        return self.url.format(_key = self.key, _query = query)

