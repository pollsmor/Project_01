#Yevgeniy Gorbachev
#SoftDev1 pd1
#K<n> -- <K<n>.__name__>
#ISO 8601 Date

from flask import *
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route('/')
def index():
    return render_template('_base.html')

app.run(debug=True)
