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

app.run(debug=True)
