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

def get_value(query):
    info = wolfram(query)
    return info['queryresult']['pods'][1]['subpods'][0]['plaintext']


#have to remove functions from class
#print(wolfram("http://api.wolframalpha.com/v2/query?appid=P4747E-2545R4KKGK&input=2^4&output=json"))


##Things to return
#plaintext
#dist, ra, rec, interesting things
#search, return first result that is a rocket (dw about this yet)
import re


def wikipedia(query):
    url = urllib.request.urlopen("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch={query}".format(query=query))
    response = url.read()
    data = json.loads(response)
    pageID = data['query']['search'][0]['pageid']

    print(pageID)

    url2 = urllib.request.urlopen("https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={pageID}".format(pageID=pageID))
    response2 = url2.read()
    data2 = json.loads(response2)
    text = data2["parse"]["text"]["*"]
    print(text.find('<table class='))
    print(re.search(re.compile('<table class=\\"infobox\\" style=\\"width:22em\\"><caption>{query}.*?><\/table>'.format(query=query)), text))
