import logging
import pymysql
from ..song_info import SongInfo

# TODO(音频编码类型字段)

init_table_ = """CREATE TABLE if not exists `musicme`.`{table_name}`  (
  `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) NULL,
  `name` varchar(128) NULL,
  `type` varchar(8) NULL,
  `ar` varchar(128) NULL,
  `al` varchar(128) NULL,
  `lyric` text NULL,
  `create_date` DATETIME(6) NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` DATETIME(6) NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX(`uuid`) USING BTREE,
  INDEX(`name`) USING BTREE
);"""

class MusicDbClient:
    db_name = 'musicme'
    table_name = 'musicme'

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
    def insert_a_song(self, info: SongInfo, uuid_:str):
        with self._conn.cursor() as cursor:
            
            sql = """INSERT INTO `musicme`.`{}` (`uuid`, `name`, `type`, `ar`, `al`, `lyric` )VALUES('{}','{}','{}','{}','{}','{}')""".format(
                self.table_name,
                uuid_,
                info.get_name(),
                info.get_type(),
                info.get_ar_name(),
                info.get_al_name(),
                info.get_lyric())
            cursor.execute(sql)
            self._conn.commit()
    
    def close(self):
        self._conn.close()
            
