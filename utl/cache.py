import sqlite3

__dbfile__ = 'data/cache.db'

# def search(query):
    
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

INIT(1)