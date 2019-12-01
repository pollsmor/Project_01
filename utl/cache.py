import sqlite3

__dbfile__ = 'data/cache.db'

# defines default order of selection
default_orders = {
    'engines': ['name', 'mass', 'impulse', 'exhaust', 'thrust', 'propellant'],
    'planets': ['name', 'distance', 'ra', 'dec'] 
}

class CacheError(Exception):
    pass

def INIT(replace=0):
    db = sqlite3.connect(__dbfile__)

    with open('utl/db_schema.txt','r') as schemaf:
        schema = schemaf.read().split('\n')
    if replace:
        for cmd in schema[3:]:
            try:
                db.execute(cmd)
            except sqlite3.OperationalError as ex:
                print(ex)
    for cmd in schema[:3]:
        db.execute(cmd)
    db.commit()
    db.close()

def search(query):
    db = sqlite3.connect(__dbfile__)
    pairs = query.items()
    

    qtype = query['type']
    del query['type']
    conds = ' AND '.join(['(%s=?)' % item[0] for item in pairs]) # generates "(col1=?) AND (col2=?) AND ..."
    args = tuple([item[1] for item in pairs])

    command = 'select %s from queries where ' + conds 
    if qtype == 'travel time':
        result = db.execute(command % 'time', args)
    elif qtype == 'fuel mass':
        result = db.execute(command % 'fuel', args)

    if len(result):
        return result[0][0]
    else:
        query['engine'] = _search_item(table='engines', name=query['engine'])
        query['origin'] = _search_item(table='planets', name=query['origin'])
        query['destination'] = _search_item(table='planets', name=query['destination'])
    
    return query

def _search_item(*args, **kwargs):
    table = kwargs['table']
    name = kwargs['name']

    order = '(%s)' % ','.join(default_orders[table])
    db = sqlite3.connect(__dbfile__)
    result = db.execute('select ? from ? where (name = ?);', (order, table, name))
    result = [item for item in result]
    if len(result):
        return dict(zip(default_orders[table], result[0])) # converts result to dictionary
    else:
        return False

def store(results):
    _insert(table='queries', values=results['results'])
    _insert(table='engines', values=results['engine'])
    _insert(table='planets', values=results['origin'])
    _insert(table='planets', values=results['destination'])

def _insert(*args, **kwargs):
    db = sqlite3.connect(__dbfile__)
    table = kwargs['table']
    values = kwargs['values'].items()

    # forms an ordering between columns and values
    # removes necessity for correctly ordering entries in values
    cols = '(%s)' % ','.join([item[0] for item in values]) # generates "(col1,col2,...)"
    contents = tuple([item[1] for item in values]) # argument tuple for insertion
    argfs = '(%s)' % ','.join(['?' for item in contents]) # generates "(?,?,...)"

    
    db.execute('insert or ignore into %s %s values %s;' % (table, cols, argfs), contents)
    db.commit()
    db.close()

INIT(1)