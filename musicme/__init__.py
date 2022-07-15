from flask import Flask
import os
from contextlib import suppress
from . import music_163
from . import db

def create_app():
    a = Flask(__name__, instance_relative_config=True)

    # 确保instance目录存在
    with suppress(OSError):
        os.makedirs(a.instance_path)

    a.config.from_pyfile('../conf/config.py')

    # 初始化本地数据库
    db.init(a)
    
    conf_path = os.path.join(a.instance_path, "../conf/server.json")
    music_163.init_music163(a, conf_path)

    return a


app = create_app()


#
from . import api
