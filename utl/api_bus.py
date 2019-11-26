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
WIKIPEDIA_PAGE_INFO = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
EXOPLANETS = API('REPLACE WITH KEY','REPLACE WITH URL')
    
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
    pageID = str(wiki(query))
    url = WIKIPEDIA_PAGE_INFO.get_url(pageID)
    info = get_json(url)
    return info

#returns thrustVac, spVac, spSL, and dryW
def get_wiki_info(query):
    if 'rocket' not in query:
        query += ' rocket'
    info = go_to_page(query)
    info = info['parse']['text']['*']                #all content of the wiki page (html)
    imp_info = {}


    ##Thrust (vac.) found in infobox
    thrustVac = info.find("Thrust (vac.)") + 22
    thrustVac_str = info[thrustVac:thrustVac+30]     #add arbitrary large number for dif sig figs
    if '&' in thrustVac_str:
        thrustVac_str = thrustVac_str.partition('&')[0]
    imp_info['thrust'] = thrustVac_str

    
    ## Isp (vac.) found in infobox
    spVac = -1
    for i in range(0, 2):
        spVac = info.find('(vac.)', spVac + 1)
    spVac += 15
    spVac_str = info[spVac:spVac+30]                  #add arbitrary large number for dif sig figs
    spVacVelocity = spVac_str
    if '&' in spVac_str or ' ' in spVac_str:
        spVac_str = str(spVac_str.partition('&')[0])
        spVac_str = spVac_str.partition(' ')[0]
    imp_info['impulse'] = spVac_str
    spVacVelocity_index = spVacVelocity.find('(')  + 1
    spVacVelocity_str = spVacVelocity[spVacVelocity_index:spVacVelocity_index+5]     #add arbitrary number for dif sig figs within range
    if '&' in spVacVelocity_str:
        spVacVelocity_str = spVacVelocity_str.partition('&')[0]
    imp_info['exhaust'] = spVacVelocity_str

    
##    ## Isp (SL) found in infobox
##    spSL = -1
##    for i in range(0, 2):
##        spSL = info.find('(SL)', spSL + 1)
##    spSL += 13
##    spSL_str = info[spSL:spSL+20]
##    #add arbitrary large number for dif sig figs
##    if '&' in spSL_str or ' ' in spSL_str:
##        spSL_str = str(spSL_str.partition('&')[0])
##        spSL_str = spSL_str.partition(' ')[0]
##    imp_info['spSL'] = spSL_str

    
    ##Dry Weight found in infobox
    dry = info.find("Dry weight") + 19
    dry_str = info[dry:dry+30]     #add arbitrary large number for dif sig figs
    if ' ' in dry_str or '&' in dry_str:
        dry_str = str(dry_str.partition('&')[0])
        dry_str = dry_str.partition(' ')[0]
    imp_info['mass'] = dry_str

    
    return imp_info


##Tests
print(get_wiki_info("merlin rocket"))
print(get_wiki_info("Rocketdyne F-1"))
print(get_wiki_info("RS-25"))


##Things to return
#wolfram: equation result
#nasa: dist, ra, rec, interesting things
#wiki: thrust, /sp(vac.), /sp(SL), dry weight


