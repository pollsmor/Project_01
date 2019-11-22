#Quaternary Star System
#Elizabeth Doss, Yevgeniy Gorbachev, Kevin Li, Emory Walsh
#SoftDev1 pd1
#P01 -- ArRESTed Development
#2019-11-14

from flask import *
from utl import search
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route('/')
def index():
    return render_template('_base.html')

@app.route('/results', methods=['GET'])
def searchResults():
    query = request.args['query']
    results = search.search(query)
    print(results)
    #a = query[0]
    results = "43598490"
    return render_template('results.html', query = query, results = results)

app.run(debug=True)
