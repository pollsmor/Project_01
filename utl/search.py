# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re
import api_bus

# maps query parameters to regular expessions
query_patterns = {
    'time':r'(time|how long)',
    'mass':r'how much (fuel|mass)',
    'goal':r'to (reach|flyby)? [\-a-z0-9]+',
    'source':r'from [\-a-z0-9]+',
    'engine':r'using [\-a-z0-9]+',
    'fuel':r'and [0-9]*.?[0-9]+ *(kg| kilograms) (of )*fuel',
    'time':r'in [0-9]+ years'
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

    def substr(match, string): # substring using span in Match object
        return string[match.span()[0]:match.span()[1]]

    def set_category(*args, **kwargs):
        category = kwargs['category']
        default = kwargs['default'] if ('default' in kwargs) else ''

        # finds parameter in query using corresponding regex, adds to parameter dictionary
        match = re.search(query_patterns[category], query)
        if match:
            params[category] = substr(match, query)
        elif default != '':
            params[category] = default
        else: # if the default action isn't specified, assumes error
            raise BadQuery(f'Query error: {category} not present')

    
    # Determine question type
    if (re.search(query_patterns['time'], query)):
        params['type'] = 'time'
        set_category(category = 'fuel')
    elif (re.search(query_patterns['mass'], query)):
        params['type'] = 'mass'
        set_category(category = 'time', default = 'minimal')
    else:
        raise BadQuery('Query error: question type not recognized')

    set_category(category = 'source', default = 'earth')
    set_category(category = 'goal')
    set_category(category = 'engine')
    
    return params
