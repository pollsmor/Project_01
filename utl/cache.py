import sqlite3

__dbfile__ = "data/cache.db"

# def search(query):
    
def cache(query):
    if query['type'] == 'travel time':
    elif query['type'] == 'fuel mass':

def _insert(*args, **kwargs):
    db = sqlite3.connect(__dbfile__)
    table = kwargs['table']
    contents = kwargs['values']
    argfs = ('?,' * len(contents))[:-1]

    db.execute(f'insert into {table} values {argfs};', contents)
