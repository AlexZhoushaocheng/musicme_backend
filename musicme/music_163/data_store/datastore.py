from .db_mariadb import MusicDbClient
from .db_minio import MinioClient
from .song_downloader import SongDownloader
from ..song_info import SongInfo
import logging
from ..configer import configer as Conf

class DataStore():
    
    def __init__(self) -> None:
        self._mariadb = MusicDbClient(*Conf.get_mariadb_info())
        self._mariadb.init_table()
        # self._mariadb.show_db_version()
        
        self._minio = MinioClient(*Conf.get_miniodb_info())
        self._minio.init_bucket()
        
        
    def store_a_song(self, info:SongInfo)->bool:
        logger = logging.getLogger(__name__)

        logger.info('正在存储歌曲{}'.format(info.get_name()))
        
        try:
            # 下载
            data = SongDownloader.download(info.get_url())
            logging.info('下载数据结束')
            
            # mariadb存储
            self._mariadb.insert_a_song(info)
            logging.info('mariadb存储结束')
            
            # minio存储
            self._minio.insert_a_song(str(info.get_origin_id()), data)
            logging.info('minio存储结束')
        except Exception as ex:
            logger.error(ex)
            return False
        return True