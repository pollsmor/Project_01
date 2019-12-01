# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re
from utl.api_bus import wolfram, wikipedia, exoplanets
from utl.cache import search as cachesearch, store

#included separately due to frequency of use and modification
planet_pattern = '[a-z]+(\-[0-9]+ ?[a-z ])?'
rocket_pattern = '(Merlin |Rocketdyne |BMW |S[0-9]\.)?[\-a-zA-Z0-9]+'

# maps query parameters to regular expessions
query_patterns = {
    'travel time':re.compile('(time|how long)',
        re.IGNORECASE),
    'fuel mass':re.compile('how much (fuel|mass)',
        re.IGNORECASE),
    'destination':re.compile('to (reach |flyby |(get|fly) to )?%s' % planet_pattern,
        re.IGNORECASE),
    'method':re.compile('to (reach|flyby|(get|fly) to)', 
        re.IGNORECASE),
    'origin':re.compile('from %s' % planet_pattern, 
        re.IGNORECASE),
    'engine':re.compile('(using|with) %s' % rocket_pattern, 
        re.IGNORECASE),
    'fuel':re.compile('(and|using) [0-9]*.?[0-9]+ tons of fuel',
        re.IGNORECASE),
    'time':re.compile('in [0-9]+ years',
        re.IGNORECASE)
}
#reduces a query parameter to raw content using the regular expression and the given function
reductions = {
    'method':(re.compile('(reach|flyby|(get|fly) to)$'), 
        lambda s: s if s == "flyby" else "reach"),
    'destination':(re.compile('( %s)$' % planet_pattern, re.IGNORECASE),
        lambda s: s[1:-1]),
    'origin':(re.compile('( %s)$' % planet_pattern, re.IGNORECASE),
        lambda s: s[1:-1]),
    'engine':(re.compile('( %s)$' % rocket_pattern, re.IGNORECASE),
        lambda s: s[1:]),
    'fuel':(re.compile('[0-9]*.?[0-9]+'),
        lambda f: float(f) * 1000),
    'time':(re.compile('[0-9]+'),
        lambda i: int(i))
}

# TODO: STORE EQUATIONS
equations = {
    'distance':'',
    'mass':'',
    'time':''
}

class BadQuery(Exception):
    pass

def search(query):
    query = _parse(query)
    result = cachesearch(query)
    if type(result) != dict:
        return result
    if not result['engine']:
        result['engine'] = wikipedia(query['engine'])
    if not result['origin']:
        result['origin'] = exoplanets(query['origin'])
    if not result['destination']:
        result['destination'] = exoplanets(query['destination'])

    # TODO: IMPLEMENT EQUATION PROCESSING
    distance = equations['distance']
    distance = wolfram(distance)
    if query['type'] == 'travel time':
        time = equations['time']
        return wolfram(time)
    elif query['type'] == 'fuel mass':
        fuel = equations['fuel']
        return wolfram(time)



def _parse(query):
    query = query.lower()
    params = {}
    params['query'] = query

    # LOCAL FUNCTIONS
    def substr(match, string): # substring using span in Match object
        return string[match.span()[0]:match.span()[1]]

    def set_category(*args, **kwargs):
        category = kwargs['category']
        default = kwargs['default'] if ('default' in kwargs) else ''

        # finds parameter in query using corresponding regex, adds to parameter dictionary
        match = re.search(query_patterns[category], query)
        if match:
            intermediate = substr(match, query)
            final_raw = substr(re.search(reductions[category][0], intermediate), intermediate)
            final = reductions[category][1](final_raw)
            params[category] = final
            # print('Reduced \"%s\" to \"%s\"' % (intermediate, final))
        elif default != '':
            params[category] = default
        else: # if the default action isn't specified, assumes error
            raise BadQuery(f'Query error: {category} not present')

    # PROCESSING
    # Determine question type
    if re.search(query_patterns['travel time'], query):
        params['type'] = 'travel time'
        set_category(category = 'fuel')
    elif re.search(query_patterns['fuel mass'], query):
        params['type'] = 'fuel mass'
        set_category(category = 'time')
    else:
        raise BadQuery('Query error: question type not recognized')

    set_category(category = 'origin', default = 'earth')
    set_category(category = 'destination')
    set_category(category = 'method', default = 'reach')
    set_category(category = 'engine')

    return params

def dict_print(d):
    print('{')
    for item in d.items():
        print('\t%s: %s' % item)
    print('}')

test_queries = [
    "how long to reach kepler-10 c using merlin 1d and 1000kg of fuel",
    "how long to get to kepler-10 d using RS-25 and 1000.2kg of fuel",
    "how much fuel to flyby kepler-10 d using RS-25 in 10 years",
    "how long to reach kepler-10 from kepler-11 using merlin 1d and 10kg of fuel"
]

# for query in test_queries:
#     try:
#         dict_print(search(query))
#     except BadQuery as badness:
#         print(badness)