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
def get_equation_result(query):
    url = WOLFRAM.get_url(query)
    info = get_json(url)
    if info['queryresult']['success'] == True:
        return info
    raise QueryFailure('Request to Wolfram\'s API failed') 

#returns result of a given equation
def wolfram(query):
    info = get_equation_result(query)
    result = info['queryresult']['pods'][1]['subpods'][0]['plaintext']
    if any(c.isalpha() for c in result):
        raise QueryFailure('Improper Request to Wolfram\'s API')
    return float(result)


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
    if 'rocket' not in query:                       #adds 'rocket' if the query does not contain it
        query += ' rocket'
    info = go_to_page(query)
    info = info['parse']['text']['*']               #all content of the wiki page (html)
    imp_info = {}

#checks to see if there is an infobox on the wiki page
    infobox = info.find('infobox')                  #all necessary info is found in the infobox of each wiki page
    #print(infobox)
    query = query.replace('rocket', '').strip().lower()
    if query.find(' ') != -1:                       #create a list of all the words in the query if more than 1
        queryList = list(query.partition(' '))
        queryList.remove(' ')
        #print(queryList)
        found = False
        while found == False and infobox != -1:     #while there is an infobox that exists and the query has not been found
            for i in queryList:                     #iterate through the words in the query
                if i in info[infobox:infobox+100].lower():
                    found = True                    #if the element is found, break and proceed
                    print('found')
                    break
            if found == False:                      #else search for another infobox
                info = info[infobox+1:]
                infobox = info.find('infobox')
                print('searching')
        if infobox == -1:                           #throws error if the page does not have an infobox with the given query
            raise QueryFailure('Incompatible Information to Wikipedia\'s API')
    else:                                           #single word query case
        while infobox != -1:
            if query not in info[infobox:infobox+100].lower():  #searches for another infobox
                info = info[infobox+1:]
                infobox = info.find('infobox')
            else:
                break                               #breaks if query found
        if infobox == -1:                           #throws error if the page does not have an infobox with the given query
            raise QueryFailure('Incompatible Information to Wikipedia\'s API')

#now we know that the query is found inside an infobox that should have the necessary information

    ##Thrust (vac.)
    thrustVac = info.find("Thrust (vac.)") + 22     #finds thrust then moves index to value
    thrustVac_str = info[thrustVac:thrustVac+30]    #add arbitrary large number for dif sig figs
    if '&' in thrustVac_str:                        #remove everything after the &
        thrustVac_str = thrustVac_str.partition('&')[0]
    imp_info['thrust'] = thrustVac_str              #add to dict


    ## Isp (vac.) and velocity
    spVac = -1
    for i in range(0, 2):                           #find the second instance of (vac.), first is for Thrust (vac.)
        spVac = info.find('(vac.)', spVac + 1)
    spVac += 15                                     #finds impulse then moves index to value
    spVac_str = info[spVac:spVac+30]
    spVacVelocity = spVac_str
    if '&' in spVac_str or ' ' in spVac_str:        #remove everything after the & or ' '
        spVac_str = str(spVac_str.partition('&')[0])
        spVac_str = spVac_str.partition(' ')[0]
    imp_info['impulse'] = spVac_str                 #add to dict
    spVacVelocity_index = spVacVelocity.find('(')  + 1  #velocity is found right after impulse in ()
    spVacVelocity_str = spVacVelocity[spVacVelocity_index:spVacVelocity_index+5]     #add arbitrary number for dif sig figs within range
    if '&' in spVacVelocity_str:                    #remove everything after the &
        spVacVelocity_str = spVacVelocity_str.partition('&')[0]
    imp_info['exhaust'] = spVacVelocity_str


    ##Dry Weight
    dry = info.find("Dry weight") + 19              #finds mass then moves index to value
    dry_str = info[dry:dry+30]
    if ' ' in dry_str or '&' in dry_str:
        dry_str = str(dry_str.partition('&')[0])    #remove everything after the & or ' '
        dry_str = dry_str.partition(' ')[0]
    imp_info['mass'] = dry_str

    imp_info['propellant'] = 'INSERT PROPELLANT'    #to be written


    return imp_info

#-----------------------Exoplanets Functions---------------------------
def exoplanets(query):
    url = EXOPLANETS.get_url(query)
    #print(url)
    info = get_json(url)

    if (len(info) <= 0): #no search results found
        raise QueryFailure('Request to NASA Exoplanet\'s API failed') 

    result = info[0]

    output = {}
    output['name'] = result['pl_name']
    output['ra'] = result['ra']
    output['dec'] = result['dec']
    output['distance'] = result['st_dist'] #in parsecs
    #print(output)
    return output

##Tests
#print(wolfram('2^4'))
#print(wolfram('why'))
#print(wikipedia("merlin 1c rocket"))
#print(wikipedia("merlin"))
#print(wikipedia("Rocketdyne F-1"))
#print(wikipedia("RS-25"))
#print(wikipedia("wow"))
#print(exoplanets('Kepler-74'))
#print(exoplanets('hi there'))



##Things to return
#wolfram alpha: equation result
#nasa exoplanet: name, ra, dec, distance
#wikipedia: thrust - Thrust (vac.), impulse - Isp (vac.), velocity - Isp (vac.) (), mass - Dry weight, propellant - Propellant
