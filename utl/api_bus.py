#import json
#from urllib.request import urlopen

import urllib.request
from urllib.parse import quote
#import json

class API(object):
    key: str
    url: str
    def __init__(self, key, url):
        self.key = key
        self.url = url

#returns url as a string  
    def get_url(self, query="") -> str:
        query = quote(query)
        return self.url.format(_key = self.key, _query = query)

#opens and reads the url query provided, url is a string
    def read(url):
        u = urlopen(url)
        response = u.read()
        info = json.loads(response)
        return info

#-----------------------Wolfram Alpha Functions---------------------------

#api_bus.wolfram(query: str) -> dict
#returns a dictionary of title and 
    def wolfram(query):
        info = read(query)
        #throw exception is success != true
        if info['queryresult']['success'] == True:
            return 'oh no'
        return info

#have to remove functions from class  
print(wolfram("http://api.wolframalpha.com/v2/query?appid=P4747E-2545R4KKGK&input=2^4&output=json"))


##Things to return
#plaintext
#dist, ra, rec, interesting things
#search, return first result that is a rocket (dw about this yet)



