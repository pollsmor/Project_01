# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [how much (fuel|mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [in {years}]*


import re

query_patterns = {
    'timeq':r'(time|how long)',
    'massq':r'how much (fuel|mass)',
    'approach':r'to (reach|flyby)? [\-a-z0-9]+',
    'src':r'from [\-a-z0-9]+',
    'engine':r'using [\-a-z0-9]+',
    'fuel':r'and [0-9]*.?[0-9]+ *kg (of )*fuel',
    'time':r'in [0-9]+ years'
}

class BadQuery(Exception):
    pass

def parse(query):
    query = query.lower()
    tokens = {}
    # Determine desired information
    if (re.search(query_patterns['timeq'], query)): # time taken
        tokens['type'] = 'timeq'
    elif (re.search(query_patterns['massq'], query)): # mass ratio
        tokens['type'] = 'massq'
    else:
        raise BadQuery('Query error: query not recognized')

    # travel information
    src = re.search(query_patterns['src'], query)
    if src:
        tokens['src'] = 'present'
    else:
        tokens['src'] = 'earth'
    
    dest = re.search(query_patterns['approach'], query)
    if dest:
        tokens['approach'] = 'present'
    else:
        raise BadQuery('Query error: destination not present')
    
    # engine query
    eng = re.search(query_patterns['engine'], query)
    if eng:
        tokens['eng'] = 'present'
    else:
        raise BadQuery('Query error: engine not present')

    # mass query
    if tokens['type'] == 'timeq':
        fuel = re.search(query_patterns['fuel'], query)
        if fuel:
            tokens['fuel'] = 'present'
        else:
            raise BadQuery('Query error: fuel not present for time query')

    # time query
    if tokens['type'] == 'massq':
        time = re.search(query_patterns['time'], query)
        if time:
            tokens['time'] = 'present'
        else:
            tokens['time'] = 'minimal'
    
    return tokens

def cons(func):
    print('Type \"quit\" to quit')
    while True:
        arg = input('> ')
        if arg == 'quit':
            break
        try:
            print(func(arg))
            print('executed successfuly')
        except Exception as ex:
            print(ex)
            
cons(parse)