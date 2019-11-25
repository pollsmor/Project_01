# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re
import api_bus

# maps query parameters to regular expessions
query_patterns = {
    'travel time':re.compile('(time|how long)'),
    'fuel mass':re.compile('how much (fuel|mass)'),
    'destination':re.compile('to (reach |flyby |(get|fly) to )?[\-a-z0-9]+'),
    'method':re.compile('to (reach|flyby|(get|fly) to)'),
    'source':re.compile('from [\-a-z0-9]+'),
    'engine':re.compile('using (merlin |rocketdyne |bmw |S[0-9]\.)?[\-a-z0-9]+'),
    'fuel':re.compile('and [0-9]*.?[0-9]+ ?(kg| kilograms) (of )?fuel'),
    'time':re.compile('in [0-9]+ years')
}
#reduces a query parameter to raw content using the regular expression and the given function
reduction_patterns = {
    'destination':(re.compile('([\-a-z0-9]+)$'), lambda s: s),
    'method':(re.compile('(reach|flyby|(get|fly) to)$'), lambda s: s if s == "flyby" else "reach"),
    'source':(re.compile('([\-a-z0-9]+)$'), lambda s: s),
    'engine':(re.compile('((merlin |rocketdyne |bmw |S[0-9]\.)?[\-a-z0-9]+)$'), lambda s: s),
    'fuel':(re.compile('[0-9]*.?[0-9]+'), lambda f: float(f)),
    'time':(re.compile('[0-9]+'), lambda i: int(i))
}

class BadQuery(Exception):
    pass

def search(query):
    query = _parse(query)
    # -- REPLACE -- # with API requests
    return query # -- REPLACE -- # with results


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
            final_raw = substr(re.search(reduction_patterns[category][0], intermediate), intermediate)
            params[category] = reduction_patterns[category][1](final_raw)
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
        set_category(category = 'time', default = 'minimal')
    else:
        raise BadQuery('Query error: question type not recognized')

    set_category(category = 'source', default = 'earth')
    set_category(category = 'destination')
    set_category(category = 'method', default = 'reach')
    set_category(category = 'engine')


    
    return params


test_queries = [
    "how long to reach kepler-10c using merlin 1d and 1000kg of fuel",
    "how long to get to kepler-10d using RS-25 and 1000.2kg of fuel",
    "how much fuel to flyby kepler-10d using RS-25 in 10 years"
]