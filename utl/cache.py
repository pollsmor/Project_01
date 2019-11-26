import sqlite3

__dbfile__ = 'data/cache.db'

# def search(query):
    
def INIT(replace=0):
    db = sqlite3.connect(__dbfile__)
    tables = ['engines','planets','timeqs','massqs']
    if replace:
        for table in tables:
            db.execute('drop table ?;', table)

    db.execute(
        '''create table engines 
        (name text primary key, 
        mass numeric, impulse numeric, thrust numeric
        img text);'''
    )
    db.execute(
        '''create table planets
        (name text primary key,  
        distance numeric, ra numeric, dec numeric);'''
    )
    db.execute(
        '''create table queries 
        (origin text, 
        method text, 
        destination text,
        engine text, 
        fuel integer, 
        time integer);'''
    )
    db.commit()
    db.close()


def store(results):
    _insert(table='queries', values=results['results'])
    _insert(table='engines', values=results['engine'])
    _insert(table='planets', values=results['origin'])
    _insert(table='planets', values=results['destination'])

def _insert(*args, **kwargs):
    table = kwargs['table']
    values = kwargs['values'].items()

    # forms an ordering between columns and values
    # removes necessity for correctly ordering entries in values
    cols = '(' + ','.join([item[0] for item in values]) + ')'
    argfs = '(' + ','.join([str(item[1]) for item in values]) + ')'

    db = sqlite3.connect(__dbfile__)
    db.execute('insert or ignore into %s %s values %s' % (table, cols, argfs))
    db.commit()
    db.close()