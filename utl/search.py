# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re
# import utl.api_bus

# maps query parameters to regular expessions
query_patterns = {
    'timeq':r'(time|how long)',
    'massq':r'how much (fuel|mass)',
    'goal':r'to (reach|flyby)? [\-a-z0-9]+',
    'source':r'from [\-a-z0-9]+',
    'engine':r'using [\-a-z0-9]+',
    'fuel':r'and [0-9]*.?[0-9]+ *(kg| kilograms) (of )*fuel',
    'time':r'in [0-9]+ years'
}

class BadQuery(Exception):
    pass

def search(query: str) -> dict:
    query = _parse(query)
    # REPLACE with API requests
    return query # REPLACE with results


def _parse(query: str) -> dict:
    query = query.lower()
    tokens = {}

    def substr(match: re.Match, string: str) -> str: # substring using span in Match object
        return string[match.span()[0]:match.span()[1]]

    def set_category(*args, **kwargs):
        category = kwargs['category']
        default = kwargs['default'] if ('default' in kwargs) else ''

        match = re.search(query_patterns[category], query)
        if match:
            tokens[category] = substr(match, query)
        elif default != '':
            tokens[category] = default
        else:
            raise BadQuery(f'Query error: {category} not present')

    # Determine question type
    if (re.search(query_patterns['timeq'], query)):
        tokens['type'] = 'timeq'
        set_category(category = 'fuel')
    elif (re.search(query_patterns['massq'], query)):
        tokens['type'] = 'massq'
        set_category(category = 'time', default = 'minimal')
    else:
        raise BadQuery('Query error: question type not recognized')

    set_category(category = 'source', default = 'earth')
    set_category(category = 'goal')
    set_category(category = 'engine')

    return tokens
