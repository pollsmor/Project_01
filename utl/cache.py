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
        for cmd in schema[3:]:
            try:
                db.execute(cmd)
            except sqlite3.OperationalError as ex:
                print(ex)
    for cmd in schema[:3]:
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

    # determines columns containing question and answer
    if query['type'] == 'travel time':
        col_query, col_answer = 'fuel', 'time'
    elif query['type'] == 'fuel mass':
        col_query, col_answer = 'time', 'fuel'
    
    cols = orders['queries'] + [col_query,]
    where = ' and '.join( [(col + '=?') for col in cols] ) # generates WHERE clause: "col1=? and col2=? and ..."
    args = tuple( map(lambda column: query[column], cols) ) # generates arguments for WHERE clause

    result = db.execute('select %s from queries where %s' % (col_answer, where), args)
    result = [item for item in result]
    if len(result):
        return result[0][0]
    else:
        result = {}
        result['origin'] = search_item(table='planets',name=query['origin'])
        result['destination'] = search_item(table='planets',name=query['destination'])
        result['engine'] = search_item(table='engines',name=query['engine'])
        return result


def store(results):
    insert(table='queries', values=results['results'])
    insert(table='engines', values=results['engine'])
    insert(table='planets', values=results['origin'])
    insert(table='planets', values=results['destination'])


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
