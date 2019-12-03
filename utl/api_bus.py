import urllib.request
from urllib.parse import quote
import json

"""Contains functions that can access and obtain the necessary info from all three APIs.

Classes:
- API: modularizes the obtaining of data from the respective APIs.

Exceptions:
- QueryFailure: custom exception that gets thrown when the query is invalid

Functions:
- get_json(url): takes a URL and returns the JSON present on that page.
- get_equation_result(query): give an equation, returns the JSON outputted by the API.
- wolfram(query): give an equation, gets the JSON from get_equation_result, returns the necessary info from the JSON.
- get_wiki_info(query): give a query, gets the page ID of the first search result on Wikipedia.
- go_to_page(query): give a query, get the page ID from get_wiki_info, returns the JSON from that page.
- wikipedia(query): returns the necessary info as a dict from the JSON obtained by go_to_page.
- exoplanets(query): give a query, obtains the necessary info from the exoplanets API as a dict.
"""

class QueryFailure(Exception):
    pass

class API(object):
    """Modularizes the obtaining of data from the respective APIs.

    Public methods:
    - get_url(url)

    Instance variables:
    - key: str
    - url: str
    """

    key: str
    url: str
    def __init__(self, key, url):
        """
        - key: the API key (if required) for accessing the API.
        - url: the base URL of the API (the API key and query can be inserted into it)
        """

        self.key = key
        self.url = url

    def get_url(self, query="") -> str:
        """Takes a query and inserts it into the link, then returns that link."""
        query = quote(query)
        return self.url.format(_key = self.key, query = query)

WOLFRAM = API('P4747E-2545R4KKGK','http://api.wolframalpha.com/v2/query?appid={_key}&input={query}&output=json')
WIKIPEDIA_SEARCH = API('','https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=search&continue=-||categories&srsearch={query}&sroffset=0')
WIKIPEDIA = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
WIKIPEDIA_PAGE_INFO = API('','https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid={query}')
EXOPLANETS = API('','https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json&where=pl_name%20like%20%27{query}%25%27')

def get_json(url):
    """Takes a URL and returns the JSON present on that page."""
    u = urllib.request.urlopen(url)
    response = u.read()
    info = json.loads(response)
    return info

#-----------------------Wolfram Alpha Functions---------------------------
#throws an error if equation fails, otherwise returns dict of info
def get_equation_result(query):
    """Give an equation, returns the JSON outputted by the API."""
    url = WOLFRAM.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API Unsuccessful, Input Proper Query')


#returns result of a given equation
def wolfram(query):
    """Give an equation, gets the JSON from get_equation_result, returns the necessary info from the JSON."""
    info = get_equation_result(query)
    result = info['queryresult']['pods'][1]['subpods'][0]['plaintext']
    if any(c.isalpha() for c in result):
        raise QueryFailure('Bad Request to Wolfram\'s API, Input Equation to Return A Number')
    return float(result)


#-----------------------Wikipedia Functions---------------------------
#returns pageID of first wiki result of query
def get_wiki_info(query):
    """Give a query, gets the page ID of the first search result on Wikipedia."""
    url = WIKIPEDIA_SEARCH.get_url(query)
    info = get_json(url)
    return str(info['query']['search'][0]['pageid'])

def go_to_page(query):
    """Give a query, get the page ID from get_wiki_info, returns the JSON from that page."""
    url = WIKIPEDIA_PAGE_INFO.get_url(get_wiki_info(query))
    return get_json(url)

#returns dict of important info
def wikipedia(query):
    """Returns the necessary info as a dict from the JSON obtained by go_to_page."""
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
    """Give a query, obtains the necessary info from the exoplanets API as a dict."""
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
#print(API.__doc__)


##Things to return
#wolfram alpha: equation result
#nasa exoplanet: name, ra, dec, distance
#wikipedia: thrust - Thrust (vac.), impulse - Isp (vac.), velocity - Isp (vac.) (), mass - Dry weight, propellant - Propellant
