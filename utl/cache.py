import sqlite3

__dbfile__ = 'data/cache.db'

# def search(query):
    
def store(results):
    if results['type'] == 'travel time':
        _insert(table='timeqs', values=results['results'])
    elif results['type'] == 'fuel mass':
        _insert(table='massqs', values=results['results'])
    
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