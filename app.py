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
    message = get_flashed_messages()
    if message:
        return render_template('_base.html', message = message[0])
    return render_template('_base.html')

@app.route('/results', methods=['GET'])
def searchResults():
    query = request.args['query']
    try:
        results = search.search(query)
        print(results)
    except search.BadQuery:
        flash("Bad query. Please try again.");
        return redirect(url_for('index'))
    return render_template('results.html', query = query, results = results)

app.run(debug=True)
