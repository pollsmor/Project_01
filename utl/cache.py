import sqlite3

__dbfile__ = 'data/cache.db'

# def search(query):
    
def store(results):
    if results['type'] == 'travel time':
        _insert(table='timeqs', values=(results['source']['name'], results['source']['name'], results['engine']['name'], results['fuel'], results['time']))
    elif results['type'] == 'fuel mass':
        _insert(table='massqs', values=(results['source']['name'], results['source']['name'], results['engine']['name'], results['time'], results['fuel']))
    _insert(table='engines', values=(results['source']))
    _insert(table='planets', values=())

def _insert(*args, **kwargs):
    table = kwargs['table']
    data = kwargs['data'].items()
    cols = '(' + ','.join([item[0] for item in data]) + ')'
    argfs = '(' + ','.join([str(item[1]) for item in data]) + ')'

    db = sqlite3.connect(__dbfile__)
    db.execute('insert into %s %s values %s' % (table, cols, argfs))
    db.commit()
    db.close()