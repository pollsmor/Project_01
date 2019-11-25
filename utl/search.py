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
    'method':re.compile('to (reach |flyby |(get|fly) to )'),
    'source':re.compile('from [\-a-z0-9]+'),
    'engine':re.compile('using (merlin |rocketdyne |bmw |S[0-9]\.)?[\-a-z0-9]+'),
    'fuel':re.compile('and [0-9]*.?[0-9]+ ?(kg| kilograms) (of )?fuel'),
    'time':re.compile('in [0-9]+ years')
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
            params[category] = substr(match, query)
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

    set_category(category = 'source', default = 'from earth')
    set_category(category = 'destination')
    set_category(category = 'method', default = 'reach')
    set_category(category = 'engine')
    
    return params
