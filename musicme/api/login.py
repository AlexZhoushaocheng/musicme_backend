from crypt import methods
from musicme import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass