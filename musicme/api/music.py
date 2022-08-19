from flask import make_response, send_file
import json
from musicme import app
from musicme import music_163
from musicme.music_163.data_store import datastore
from . import downloader
import uuid


@app.route('/hello')
def hello():
    return 'hello'

# 从云中搜索
@app.route('/search/<keyworld>',  methods=['GET', 'POST'])
def search(keyworld):
    cli = music_163.get_netEaseClient()
    songs = cli.search(keyworld)
    return songs

# 将云中的音乐保存到本地仓库
@app.route('/save/<song_id>', methods=['GET', 'POST'])
def save(song_id):
    cli = music_163.get_netEaseClient()
    info = cli.query_song_info(song_id)

    try:
        uid = str(uuid.uuid1(node=1)).replace('-','')
        # uid_ = '',json(uid.split('-'))
        data = downloader.download(info.get_url())
        music_163.get_dbcli().insert_a_song(info, uid)
        app.logger.info('保存音乐信息成功')
        
        music_163.get_dbcli().insert_a_song(info)
        
    except Exception as ex:
        app.logger.error(ex)
        return 'internal error', 400
    
    return 'ok', 200

# 上传音乐到本地仓库
@app.route('/upload/song', methods=['POST'])
def upload_song():
    pass

# 从云中下载音乐
@app.route('/download/<song_id>')
def download(song_id):
    cli = music_163.get_netEaseClient()
    info = cli.query_song_info(song_id)
    data = downloader.download(info.get_url())
    # filename = '{}.{}'.format(info.get_name(), info.get_type())
    res = make_response()
    res.data = data
    res.mimetype = 'audio/*'
    res.headers["Content-Disposition"] = "attachment; filename={}.{}".format(info.get_name().encode().decode('latin-1'), info.get_type())
    
    return res
