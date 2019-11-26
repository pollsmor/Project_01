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

WOLFRAM = API('P4747E-2545R4KKGK','http://api.wolframalpha.com/v2/query?appid={_key}&input={query}&output=json')
WIKIPEDIA_SEARCH = API('','https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=search&continue=-||categories&srsearch={query}&sroffset=0')
WIKIPEDIA = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
EXOPLANETS = API('','https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json&where=pl_name%20like%20%27{query}%25%27')

    #opens and reads the url query provided, url is a string
def get_json(url):
    u = urllib.request.urlopen(url)
    response = u.read()
    info = json.loads(response)
    return info

#-----------------------Wolfram Alpha Functions---------------------------

#api_bus.wolfram(query: str) -> dict
#this is not explicitly called, only get_equation_result is
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
    url = WIKIPEDIA_SEARCH.get_url(query)
    info = get_json(url)
    pageID = info['query']['search'][0]['pageid']
    return pageID

def go_to_page(query):
    url = WIKIPEDIA.get_url(query)
    info = get_json(url)
    pageID = wiki(query)
    return 'return from text'


    #raise QueryFailure('Request to Wolfram\'s API failed')

#print(wiki("dog"))

#-----------------------Exoplanets Functions---------------------------
def exoplanets(query):
    url = EXOPLANETS.get_url(query)
    print(url)
    info = get_json(url)

    if (len(info) <= 0): #no search results found
        print("No search results found.")
        return;

    result = info[0]

    output = {}
    output['name'] = result['pl_name']
    output['ra'] = result['ra']
    output['dec'] = result['dec']
    output['distance'] = result['st_dist'] #in parsecs
    print(output)
    return output

#have to remove functions from class
#print(wolfram("http://api.wolframalpha.com/v2/query?appid=P4747E-2545R4KKGK&input=2^4&output=json"))


##Things to return
#plaintext
#dist, ra, rec, interesting things
#search, return first result that is a rocket (dw about this yet)
#wiki: thrust, /sp(vac.), /sp(SL), dry weight
