# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re
from api_bus import wolfram, wikipedia, exoplanets, QueryFailure
from cache import search as cachesearch, insert

#included separately due to frequency of use and modification
planet_pattern = '[a-z]+(\-[0-9]+ ?([a-z][^a-z])?)?'
rocket_pattern = '(Merlin |Rocketdyne |BMW |S[0-9]\.)?[\-a-zA-Z0-9]+'
parsec = int(3.086 * (10 ** 13))
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
    'fuel':re.compile('(and|using) [0-9]*.?[0-9]+( ?kg| kilograms| tons) of fuel',
        re.IGNORECASE),
    'time':re.compile('in [0-9]+ (years|millenia)',
        re.IGNORECASE)
}
#reduces a query parameter to raw content using the regular expression and the given function
reductions = {
    'method':(re.compile('(reach|flyby|(get|fly) to)$'), 
        lambda s, m: s if s == 'flyby' else 'reach'),
    'destination':(re.compile('( %s)$' % planet_pattern, re.IGNORECASE),
        lambda s, m: s[1:-1]),
    'origin':(re.compile('( %s)$' % planet_pattern, re.IGNORECASE),
        lambda s, m: s[1:-1]),
    'engine':(re.compile('( %s)$' % rocket_pattern, re.IGNORECASE),
        lambda s, m: s[1:]),
    'fuel':(re.compile('[0-9]*.?[0-9]+'),
        lambda f, m: float(f) * 1000 if 'tons' in m else 1),
    'time':(re.compile('[0-9]+'),
        lambda i, m: float(i) * 1000 if 'millenia' in m else 1)
}
# mathematical expressions to send to Wolfram|Alpha
expressions = {
    'distance':'Sqrt{{ {dist1}^2 + {dist2}^2 - 2*{dist1}*{dist2}Sin{{{ra1} degrees}}Sin{{{ra2} degrees}}Cos{{{decdiff} degrees}} + Cos{{{ra1} degrees}}Cos{{{ra2} degrees}} }}',
    'reach': {
        'fuel':'{end}*Exp{{(2*({dist})/({exh}*{time}))}}',
        'time':'2*({dist})/({exh}*Ln{{({start})/({end})}})'
    },
    'flyby': {
        'fuel':'{end}*Exp{{(({dist})/({exh}*{time}))}}',
        'time':'({dist})/({exh}*Ln{{({start})/({end})}})'
    }
}

class BadQuery(Exception):
    pass

def search(query):
    query = _parse(query)
    print(query)
    result = cachesearch(query)
    if type(result) != dict:
        return result
    
    # uses APIs to find data not found in cache
    if not result['engine']:
        try:
            result['engine'] = wikipedia(query['engine'])
            insert(table='engines', values=result['engine'])
        except QueryFailure as qf:
            raise
    if not result['origin']:
        try:
            result['origin'] = exoplanets(query['origin'])
            insert(table='planets', values=result['origin'])
        except QueryFailure as qf:
            raise
    if not result['destination']:
        try:
            result['destination'] = exoplanets(query['destination'])
            insert(table='planets', values=result['destination'])
        except QueryFailure as qf:
            raise

    # Substitutes numbers into distance expression
    distance = expressions['distance'].format(
        dist1 = int(result['origin']['distance'] * parsec),
        dist2 = int(result['destination']['distance'] * parsec),
        ra1 = result['origin']['ra'],
        ra2 = result['destination']['ra'],
        decdiff = int(result['origin']['dec'] - result['destination']['dec'])
    )

    # generates full expression corresponding to query
    if query['type'] == 'travel time':
        expr = expressions[query['method']]['time'].format(
            dist=distance,
            exh=result['engine']['exhaust'],
            end=result['engine']['mass'] + 10,
            start = query['fuel'] + result['engine']['mass'] + 10
        )
    elif query['type'] == 'fuel mass':
        expr = expressions[query['method']]['fuel'].format(
            dist=distance,
            exh=result['engine']['exhaust'],
            end=result['engine']['mass'] + 10,
            time=query['time']
        )
    
    try:
        query['result'] = wolfram(expr)
        return query
    except QueryFailure as qf:
        raise



def _parse(query):
    # query = query.lower()
    params = {}
    params['query'] = query

    def substr(match, string): # substring using span in Match object
        return string[match.span()[0]:match.span()[1]]

    def set_category(*args, **kwargs):
        # Finds keywords for a category in query string
        # Adds corresponding data to parameters dictionary
        category = kwargs['category']
        default = kwargs['default'] if ('default' in kwargs) else ''

        match = re.search(query_patterns[category], query)
        if match:
            intermediate = substr(match, query)
            final_raw = substr(re.search(reductions[category][0], intermediate), intermediate)
            final = reductions[category][1](final_raw, intermediate)
            params[category] = final
        elif default != '':
            params[category] = default
        else: # if the default action isn't specified, assumes error
            raise BadQuery('Query error: %s not present' % category)

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
