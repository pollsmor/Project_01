#Quaternary Star System
#Elizabeth Doss, Yevgeniy Gorbachev, Kevin Li, Emory Walsh
#SoftDev1 pd1
#P01 -- ArRESTed Development
#2019-11-14

from flask import *
from utl import search
from os import urandom
from keys import WFAkey # need a separate keys.py to import from, putting it in here makes app.py run twice

app = Flask(__name__)
app.secret_key = urandom(32) # won't be necessary for this project as we aren't using sessions

if len(WFAkey) == 0:
    print("You are missing an API key. More information is provided on the root page.")

@app.route('/')
def index():
    if len(WFAkey) == 0:
        return render_template('getakey.html')

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
        flash("Bad query. Please try again.")
        return redirect(url_for('index'))
    return render_template('results.html', query = query, results = results)

app.run(debug=True)
