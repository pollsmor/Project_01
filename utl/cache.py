import sqlite3

__dbfile__ = 'data/cache.db'

# defines default order of selection
orders = {
    'engines': ['name', 'mass', 'impulse', 'exhaust', 'thrust', 'propellant'],
    'planets': ['name', 'distance', 'ra', 'dec'],
    'queries': ['origin','method','destination','engine'] 
}

class CacheError(Exception):
    pass

def INIT(replace=0):
    db = sqlite3.connect(__dbfile__)

    with open('utl/db_schema.txt','r') as schemaf:
        schema = schemaf.read().split('\n')
    if replace:
        for cmd in schema[2:]:
            try:
                db.execute(cmd)
            except sqlite3.OperationalError as ex:
                print(ex)
    for cmd in schema[:2]:
        db.execute(cmd)
    db.commit()
    db.close()


def search(query): # searches db for query

    def search_item(*args, **kwargs):
        table = kwargs['table']
        name = kwargs['name']

        order = ','.join(orders[table])
        db = sqlite3.connect(__dbfile__)
        result = db.execute('select %s from %s where name=?;' % (order, table), (name,))
        result = [item for item in result]
        if len(result):
            return dict(zip(orders[table], result[0])) # converts result to dictionary
        else:
            return False
    
    db = sqlite3.connect(__dbfile__)

    result = {}
    result['origin'] = search_item(table='planets',name=query['origin'])
    result['destination'] = search_item(table='planets',name=query['destination'])
    result['engine'] = search_item(table='engines',name=query['engine'])

    return result

def insert(*args, **kwargs):
    db = sqlite3.connect(__dbfile__)
    table = kwargs['table']
    values = kwargs['values'].items()

    # forms an ordering between columns and values
    # removes necessity for correctly ordering entries in values
    cols = '(%s)' % ','.join([item[0] for item in values]) # generates "(col1,col2,...)"
    contents = tuple([item[1] for item in values]) # argument tuple for insertion
    argfs = '(%s)' % ','.join(['?' for item in contents]) # generates "(?,?,...)"

    cmd = 'insert or ignore into %s %s values %s;' % (table, cols, argfs)
    db.execute(cmd, contents)
    db.commit()
    db.close()
