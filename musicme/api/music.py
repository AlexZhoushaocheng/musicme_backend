from musicme import app
from musicme import music_163

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/search')
def search():
    cli = music_163.get_netEaseClient()
    songs = cli.search('等一分钟')
    return songs