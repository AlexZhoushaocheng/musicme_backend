import logging
import pymysql
from ..song_info import SongInfo

# TODO(音频编码类型字段)

init_table_ = """CREATE TABLE if not exists `musicme`.`{table_name}`  (
  `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `origin_id` bigint(255) UNSIGNED NULL,
  `name` varchar(255) NULL,
  `ar` varchar(255) NULL,
  `al` varchar(255) NULL,
  `lyric` text NULL,
  `create_date` DATETIME(6) NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` DATETIME(6) NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX(`origin_id`) USING BTREE,
  INDEX(`name`) USING BTREE
);"""

class MusicDbClient:
    db_name = 'musicme'
    table_name = 'music'

    def __init__(self, host, port, user, password) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._conn = pymysql.connect(host=host, port=port, user= user, password=password, database=self.db_name)
        

    def show_db_version(self) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT VERSION()')
            print(cursor.fetchone())

    def init_table(self):
        with self._conn.cursor() as cursor:
            cursor.execute(init_table_.format(table_name=self.table_name))
    
    # 添加一首歌
    def insert_a_song(self, info: SongInfo):
        with self._conn.cursor() as cursor:
            sql = """INSERT INTO `musicme`.`music` ( `origin_id`, `name`, `ar`, `al`, `lyric` )VALUES({},'{}','{}','{}','{}')""".format(
                info.get_origin_id(),
                info.get_name(),
                info.get_ar_name(),
                info.get_al_name(),
                info.get_lyric())
            cursor.execute(sql)
            self._conn.commit()
    
    def close(self):
        self._conn.close()
            
