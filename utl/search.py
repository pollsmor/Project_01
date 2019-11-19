# Expected time query format (asterisks represent optional parameters):
# [(time|how long)] [to (reach|flyby)]* [from {planet}]* [to {planet}] [using {engine}] [and {fuel mass} of fuel]
# Expected mass query format:
# [“how much fuel”, “how much mass”] [to “reach”, “flyby”]* [from {planet}]* [to {planet}] [using {engine}]

import re

class BadQuery(Error):
    pass

query_patterns = {
    'time':r'(time|how long)',
    'mass':r'(how much fuel|how much mass)',
    'approach':r'to (reach|flyby)',
    'source':r'from [\-a-z0-9]+',
    'dest':r'to ][\-a-z0-9]+',
    'engine':r'using [\-a-z0-9]+'
    'fuel':r'and [0-9]*.?[0-9]+ *kg (of )*fuel'
}

def parse(query: str):
    query = query.lower()