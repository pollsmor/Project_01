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
    db = sqlite3.connect(__dbfile__)

    table = kwargs['table']
    cols = "("
    contents = kwargs['values']
    argfs = ('?,' * len(contents))[:-1]

    db.execute(f'insert into {table} values ({argfs});', contents)
    db.commit()
    db.close()
