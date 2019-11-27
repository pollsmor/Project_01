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

#BASES
WOLFRAM = API('P4747E-2545R4KKGK','http://api.wolframalpha.com/v2/query?appid={_key}&input={query}&output=json')
WIKIPEDIA_SEARCH = API('','https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=search&continue=-||categories&srsearch={query}&sroffset=0')
WIKIPEDIA = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
WIKIPEDIA_PAGE_INFO = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
EXOPLANETS = API('','https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json&where=pl_name%20like%20%27{query}%25%27')

#opens and reads the url query provided, url is a string
def get_json(url):
    u = urllib.request.urlopen(url)
    response = u.read()
    info = json.loads(response)
    return info

#-----------------------Wolfram Alpha Functions---------------------------
#throws an error if equation fails, otherwise returns dict of info
def wolfram(query):
    url = WOLFRAM.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API failed') 

#returns result of a given equation
def get_equation_result(query):
    info = wolfram(query)
    return info['queryresult']['pods'][1]['subpods'][0]['plaintext']

#-----------------------Wikipedia Functions---------------------------
#returns pageID of first wiki result of query
def wiki(query):
    url = WIKIPEDIA_SEARCH.get_url(query)
    info = get_json(url)
    pageID = info['query']['search'][0]['pageid']
    return pageID

#returns dict of info
def go_to_page(query):
    pageID = str(wiki(query))
    url = WIKIPEDIA_PAGE_INFO.get_url(pageID)
    info = get_json(url)
    return info

#returns thrustVac, spVac, and dryW
def get_wiki_info(query):
    #adds 'rocket' if the query does not contain it
    if 'rocket' not in query:
        query += ' rocket'
    info = go_to_page(query)
    info = info['parse']['text']['*']                #all content of the wiki page (html)
    imp_info = {}

#checks to see if there is an infobox on the wiki page
    infobox = info.find('infobox')
    while infobox != -1:                            #searches through all of info to see if there are multiple infoboxes, one with the proper query
        query = query.replace('rocket', '').strip()
        if query not in info[infobox:infobox+100].lower():
            info = info[infobox+1:]
            infobox = info.find('infobox')
        else break
    if inbox == -1:                                   #throws error if the page does not have an infobox with the given query
        raise QueryFailure('Incompatible Information to Wikipedia\'s API')

    ##Thrust (vac.) found in infobox
    thrustVac = info.find("Thrust (vac.)") + 22
    thrustVac_str = info[thrustVac:thrustVac+30]     #add arbitrary large number for dif sig figs
    if '&' in thrustVac_str:                         #remove everything after the &
        thrustVac_str = thrustVac_str.partition('&')[0]
    imp_info['thrust'] = thrustVac_str


    ## Isp (vac.) found in infobox
    spVac = -1
    for i in range(0, 2):                           #find the second instance of (vac.) because the first is for Thrust (vac.)
        spVac = info.find('(vac.)', spVac + 1)
    spVac += 15
    spVac_str = info[spVac:spVac+30]
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


    ##Dry Weight found in infobox
    dry = info.find("Dry weight") + 19
    dry_str = info[dry:dry+30]
    if ' ' in dry_str or '&' in dry_str:
        dry_str = str(dry_str.partition('&')[0])
        dry_str = dry_str.partition(' ')[0]
    imp_info['mass'] = dry_str

    imp_info['propellant'] = 'INSERT PROPELLANT'    #to be written


    return imp_info

#-----------------------Exoplanets Functions---------------------------
def exoplanets(query):
    url = EXOPLANETS.get_url(query)
    print(url)
    info = get_json(url)

    if (len(info) <= 0): #no search results found
        print("No search results found.")

    result = info[0]

    output = {}
    output['name'] = result['pl_name']
    output['ra'] = result['ra']
    output['dec'] = result['dec']
    output['distance'] = result['st_dist'] #in parsecs
    print(output)
    return output

##Tests
#print(get_wiki_info("merlin 1c rocket"))
#print(get_wiki_info("merlin"))
#print(get_wiki_info("Rocketdyne F-1"))
#print(get_wiki_info("RS-25"))
#print(get_wiki_info("wow"))


##Things to return
#wolfram: equation result
#nasa: dist, ra, rec, interesting things
#wiki: thrust, /sp(vac.), /sp(SL), dry weight
