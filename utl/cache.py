import sqlite3

__dbfile__ = 'data/cache.db'

def INIT(replace=0):
    db = sqlite3.connect(__dbfile__)
    schemaf = open('utl/db_schema.txt','r')
    schema = schemaf.read()
    print(schema)
    schema = schema.split('\n')
    if replace:
        for cmd in schema[3:]:
            try:
                print(cmd)
                db.execute(cmd)
            except sqlite3.OperationalError as ex:
                print(ex)
    for cmd in schema[:3]:
        print(cmd)
        db.execute(cmd)
    db.commit()
    db.close()

def _search_one(*args, **kwargs):
    table = kwargs['table']
    query = kwargs['data'].items()

    # generates selection order
    cols = [item[0] for item in query]
    cols = '(%s)' % (','.join(cols))
    
    # generates 'WHERE' clause
    where = ['(%s=?)' % item[0] for item in query]
    where = ' AND '.join(where)

    args = tuple([item[1] for item in query])
    
    db = sqlite3.connect(__dbfile__)
    result = db.execute('select %s from %s where %s;' % (cols, table, where), args)
    if len(result):
        return result[1]
    else:
        return False
    db.close()


def _store(results):
    _insert(table='queries', values=results['results'])
    _insert(table='engines', values=results['engine'])
    _insert(table='planets', values=results['origin'])
    _insert(table='planets', values=results['destination'])

def _insert(*args, **kwargs):
    table = kwargs['table']
    values = kwargs['values'].items()

    # forms an ordering between columns and values
    # removes necessity for correctly ordering entries in values
    cols = '(%s)' % ','.join([item[0] for item in values])
    contents = tuple([item[1] for item in values])
    argfs = '(%s)' % ','.join(['?' for item in contents])

    db = sqlite3.connect(__dbfile__)
    db.execute('insert or ignore into %s %s values %s' % (table, cols, argfs), contents)
    db.commit()
    db.close()

INIT(1)