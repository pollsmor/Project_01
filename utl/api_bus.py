#import json
#from urllib.request import urlopen

import urllib.request
from urllib.parse import quote
import json

class QueryFailure(Exception):
    pass

class API(object):
    key: str
    url: str
    def __init__(self, key, url):
        self.key = key
        self.url = url

    #given a string query, returns the api request url as a string  
    def get_url(self, query="") -> str:
        query = quote(query)
        return self.url.format(_key = self.key, query = query)

WOLFRAM = API('P4747E-2545R4KKGK','http://api.wolframalpha.com/v2/query?appid={_key}&input={_query}&output=json')
WIKIPEDIA = API('REPLACE WITH KEY','REPLACE WITH URL')
EXOPLANETS = API('REPLACE WITH KEY','REPLACE WITH URL')

#opens and reads the url query provided, url is a string
def get_json(url):
    u = urllib.requesturlopen(url)
    response = u.read()
    info = json.loads(response)
    return info

#-----------------------Wolfram Alpha Functions---------------------------

#api_bus.wolfram(query: str) -> dict
#returns a dictionary of title and 
def wolfram(query):
    url = WOLFRAM.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API failed')

def get_equation_result(query):
    info = wolfram(query)
    return info['queryresult']['pods'][1]['subpods'][0]['plaintext']

#-----------------------Wikipedia Functions---------------------------
def wiki(query):
    url = WIKIPEDIA.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API failed')


#have to remove functions from class  
#print(wolfram("http://api.wolframalpha.com/v2/query?appid=P4747E-2545R4KKGK&input=2^4&output=json"))


##Things to return
#plaintext
#dist, ra, rec, interesting things
#search, return first result that is a rocket (dw about this yet)
#wiki: thrust, /sp(vac.), /sp(SL), dry weight


