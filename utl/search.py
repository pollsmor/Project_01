# Expected time query format (asterisks represent optional parameters) (case insensitive):
# [(time|how long)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [(how much fuel|how much mass)] [to (reach|flyby)* {planet}] [from {planet}]* [using {engine}]


import re

query_patterns = {
    'time':r'(time|how long)',
    'mass':r'(how much fuel|how much mass)',
    'approach':r'to (reach|flyby)? [\-a-z0-9]+',
    'src':r'from [\-a-z0-9]+',
    'engine':r'using [\-a-z0-9]+',
    'fuel':r'and [0-9]*.?[0-9]+ *kg (of )*fuel'
}

class BadQuery(Exception):
    pass

def parse(query):
    query = query.lower()
    tokens = {}
    # Determine desired information
    if (re.search(query_patterns['time'], query)): # time taken
        tokens['type'] = 'time'
    elif (re.search(query_patterns['time'], query)): # mass ratio
        tokens['type'] = 'massr'
    else:
        raise BadQuery('infostring not recognized')

    # travel information
    src = re.search(query_patterns['src'], query)
    if src:
        tokens['src'] = 'origin present'
    
    dest = re.search(query_patterns['approach'], query)
    if dest:
        tokens['approach'] = 'approach present'
    else:
        raise BadQuery('destination not present')
    
    # engine query
    eng = re.search(query_patterns['engine'], query)
    if eng:
        tokens['eng'] = 'eng present'
    else:
        raise BadQuery('engine not present')

    # mass query
    if tokens['type'] == 'time':
        fuel = re.search(query_patterns['fuel'], query)
        if fuel:
            tokens['fuel'] = 'fuel present'
        else:
            raise BadQuery('fuel not present for time query')
    return tokens

print('Type \"quit\" to quit')
while True:
    arg = input('> ')
    if arg == 'quit':
        break
    try:
        print(parse(arg))
        print('successfully parsed')
    except BadQuery as qerror:
        print(qerror)