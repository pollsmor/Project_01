#import json
#from urllib.request import urlopen

import urllib.request
from urllib.parse import quote
import json
import re
from keys import WFAkey

class QueryFailure(Exception):
    pass

class API(object):
    key: str
    url: str
    def __init__(self, key, url):
        self.key = key
        self.url = url

    def get_url(self, query="") -> str:
        query = quote(query)
        return self.url.format(_key = self.key, query = query)

WOLFRAM = API(WFAkey,'http://api.wolframalpha.com/v2/query?appid={_key}&input={query}&output=json')
WIKIPEDIA_SEARCH = API('','https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=search&continue=-||categories&srsearch={query}&sroffset=0')
WIKIPEDIA = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
WIKIPEDIA_PAGE_INFO = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
EXOPLANETS = API('','https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json&where=pl_name%20like%20%27{query}%25%27')

def get_json(url):
    u = urllib.request.urlopen(url)
    response = u.read()
    info = json.loads(response)
    return info

#-----------------------Wolfram Alpha Functions---------------------------
#throws an error if equation fails, otherwise returns dict of info
def get_equation_result(query):
    url = WOLFRAM.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API Unsuccessful, Input Proper Query')

def substr(match, string): # substring using span in Match object
    return string[match.span()[0]:match.span()[1]]

#returns result of a given equation
def wolfram(query):
    info = get_equation_result(query)
    response = info['queryresult']['pods'][1]['subpods'][0]['plaintext']
    if ('...' in response):
        dec = response[:response.find('...')]
        expon = response[response.find('^')+1:]
        response = float(dec) * 10 ** float(expon)
        print(response)
    if any(c.isalpha() for c in response):
        raise QueryFailure('Bad Request to Wolfram\'s API, Input Equation to Return A Number')
    return float(response)


#-----------------------Wikipedia Functions---------------------------
#returns pageID of first wiki result of query
def get_wiki_info(query):
    url = WIKIPEDIA_SEARCH.get_url(query)
    info = get_json(url)
    return str(info['query']['search'][0]['pageid'])

#returns dict of info
def go_to_page(query):
    url = WIKIPEDIA_PAGE_INFO.get_url(get_wiki_info(query))
    return get_json(url)

#returns dict of important info
def wikipedia(query):
    if 'rocket' not in query:
        query += ' rocket'
    info = go_to_page(query)
    info = info['parse']['text']['*']               #all content of the wiki page (html)
    imp_info = {}

    infobox = info.find('infobox')
    #print(infobox)
    query = query.replace('rocket', '').strip().lower()
    if query.find(' ') != -1:                       #create a list of all the words in the query if more than 1
        queryList = list(query.partition(' '))
        queryList.remove(' ')
        #print(queryList)
        found = False
        while found == False and infobox != -1:
            for i in queryList:
                if i in info[infobox:infobox+100].lower():
                    found = True
                    print('found')
                    break
            if found == False:
                info = info[infobox+1:]
                infobox = info.find('infobox')
                print('searching')
        if infobox == -1:                           #throws error if the page does not have an infobox with the given query
            raise QueryFailure('Incompatible Information to Wikipedia\'s API')
    else:
        while infobox != -1:
            if query not in info[infobox:infobox+100].lower():
                info = info[infobox+1:]
                infobox = info.find('infobox')
            else:
                break
        if infobox == -1:
            raise QueryFailure('Incompatible Information to Wikipedia\'s API')

    #the query is found inside an infobox that should have all necessary information

    infobox += 37
    name_str = info[infobox:infobox+50]             #add arbitrary large number for dif name lengths
    #print(name_str)
    if '<' in name_str:
        name_str = name_str.partition('<')[0]
    imp_info['name'] = name_str


    ##Thrust (vac.)
    thrustVac = info.find("Thrust (vac.)") + 22
    thrustVac_str = info[thrustVac:thrustVac+30]
    if '&' in thrustVac_str:
        thrustVac_str = thrustVac_str.partition('&')[0]
    imp_info['thrust'] = thrustVac_str


    ## Isp (vac.) and velocity
    spVac = -1
    for i in range(0, 2):                           #find the second instance of (vac.), first is for Thrust (vac.)
        spVac = info.find('(vac.)', spVac + 1)
    spVac += 15
    spVac_str = info[spVac:spVac+30]
    spVacVelocity = spVac_str
    if '&' in spVac_str or ' ' in spVac_str:
        spVac_str = str(spVac_str.partition('&')[0])
        spVac_str = spVac_str.partition(' ')[0]
    imp_info['impulse'] = spVac_str
    spVacVelocity_index = spVacVelocity.find('(')  + 1  #velocity is found right after impulse in ()
    spVacVelocity_str = spVacVelocity[spVacVelocity_index:spVacVelocity_index+5]
    if '&' in spVacVelocity_str:
        spVacVelocity_str = spVacVelocity_str.partition('&')[0]
    imp_info['exhaust'] = spVacVelocity_str


    ##Dry Weight
    dry = info.find("Dry weight") + 19
    dry_str = info[dry:dry+30]
    if ' ' in dry_str or '&' in dry_str:
        dry_str = str(dry_str.partition('&')[0])
        dry_str = dry_str.partition(' ')[0]
    imp_info['mass'] = dry_str

    imp_info['propellant'] = 'INSERT PROPELLANT'


    return imp_info

#-----------------------Exoplanets Functions---------------------------
def exoplanets(query):
    url = EXOPLANETS.get_url(query)
    #print(url)
    info = get_json(url)

    if (len(info) <= 0): #no search results found
        raise QueryFailure('Bad Request to NASA Exoplanet\'s API failed')

    result = info[0]

    output = {}
    output['name'] = result['pl_name']
    output['ra'] = result['ra']
    output['dec'] = result['dec']
    output['distance'] = result['st_dist']
    #print(output)
    return output

##Tests
#print(wolfram('2^4'))
#print("\n")
#print(wolfram('why'))
#print(wikipedia("merlin"))
#print(wikipedia("Rocketdyne F-1"))
#print(wikipedia("RS-25"))
#print(wikipedia("wow"))
#print("\n")
#print(exoplanets('Kepler-74'))
#print(exoplanets("Proxima"))
#print(exoplanets('hi there'))


##Things to return
#wolfram alpha: equation result
#nasa exoplanet: name, ra, dec, distance
#wikipedia: thrust - Thrust (vac.), impulse - Isp (vac.), velocity - Isp (vac.) (), mass - Dry weight, propellant - Propellant
