import sqlite3
import click
from flask import Flask, g, current_app
from flask.cli import with_appcontext
import os

# 数据库模块初始化
def init(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db()->sqlite3.Connection:
    if 'sqlite' not in g:
        db_path = os.path.join(current_app.instance_path, current_app.config['DATABASE_SQLITE'])
        g.sqlite = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    return g.sqlite

def close_db(e=None):
    db:sqlite3.Connection = g.pop('sqlite', None)
    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    with current_app.open_instance_resource('../sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')