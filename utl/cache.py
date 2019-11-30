import sqlite3

__dbfile__ = 'data/cache.db'

# defines default order of selection
default_orders = {
    'engines': ['name', 'mass', 'impulse', 'exhaust', 'thrust', 'img', 'propellant'],
    'planets': ['name', 'distance', 'ra', 'dec'] 
}

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
    # should: compare the query against the entries in queries
    # if the match isn't perfect, find extant entries in planets and engines
    # if matches aren't found, value False
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
    table = kwargs['table']
    values = kwargs['values'].items()

    # forms an ordering between columns and values
    # removes necessity for correctly ordering entries in values
    cols = '(%s)' % ','.join([item[0] for item in values]) # generates "(col1,col2,...)"
    contents = tuple([item[1] for item in values]) # argument tuple for insertion
    argfs = '(%s)' % ','.join(['?' for item in contents]) # generates "(?,?,...)"

    db = sqlite3.connect(__dbfile__)
    db.execute('insert or ignore into %s %s values %s;' % (table, cols, argfs), contents)
    db.commit()
    db.close()

INIT(1)