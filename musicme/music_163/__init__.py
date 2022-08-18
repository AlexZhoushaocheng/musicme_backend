# from . import nete_client
# from . import song_info
from .setting import Setting
from .data_store.db_mariadb import MusicDbClient
from .data_store.db_minio import MinioClient
from . import net_ease
import os
import json
from flask import current_app, g, Flask

# mariadb_cli
setting_ = Setting()

def init_music163(app:Flask, conf_path):
    with app.app_context():
        # 加载配置
        try:
            setting_.from_file(conf_path)
        except Exception as ex:
            app.logger.error('load config file error.')
    
        # 初始化信息数据库
        try:
            db_cli = get_dbcli()
            db_cli.init_table()
            app.logger.info('init mariadb success.')
        except Exception as ex:
            app.logger.error('init mariadb failed.', ex)
            
        # 初始化文件数据
        try:
            minio_cli = get_minio()
            minio_cli.init_bucket()
            app.logger.info('init minio success.')
        except Exception as ex:
            app.logger.error('init minio failed.', ex)
    
        app.teardown_appcontext(close_db)

        get_netEaseClient()
        app.teardown_appcontext(close_proxy)
        
        
def get_dbcli():
    if 'db' not in g:
        g.db = MusicDbClient(*setting_.mariadb_info)

    return g.db 

def get_minio()->MinioClient:
    if 'minio' not in g:
        g.minio = MinioClient(*setting_.miniodb_info)
        
    return g.minio

def close_db(e=None):
    db:"MusicDbClient" = g.pop('db', None)
    if db is not None:
        db.close()

    g.pop('minio', None)
    

def get_netEaseClient():
    if 'proxy' not in g:
        proxy_path = os.path.join(
            current_app.instance_path, "../tools", setting_.proxy_path)
        driver_path = os.path.join(
            current_app.instance_path, "../tools", setting_.driver_path_edge)
        print(proxy_path)
        print(driver_path)
        g.proxy = net_ease.ProxyAndDriver(proxy_path, driver_path)

    nete_cli = net_ease.NetEase(*g.proxy.getEdgeDriver())
    return nete_cli

def close_proxy(e=None):
    proxy:"net_ease.ProxyAndDriver" = g.pop('proxy', None)
    if proxy is not None:
        proxy.stop()
