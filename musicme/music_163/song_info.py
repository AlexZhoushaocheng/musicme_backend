import json
import logging

class SongInfo:
    # 歌曲连接
    _url = ''
    
    # 图片链接
    _pic_url = ''
    
    # 歌曲名称
    _name = ''
    _origin_id:int
    _ar_name = ''
    _al_name = ''

    def isValid(self):
        return self._valid
    
    def get_url(self):
        return self._url
    
    def get_pic_url(self):
        return self._pic_url
    
    def get_type(self):
        return self._type
    
    def get_name(self):
        return self._name
    
    def get_origin_id(self):
        return self._origin_id
    
    def get_ar_name(self):
        return self._ar_name
    
    def get_al_name(self):
        return self._al_name
    
    def get_lyric(self):
        return self._lyric
    
    def get_type(self):
        return self._type

    def __init__(self,url_detail:str, lyric:str, detail:str) -> None:
        self._valid = False
        self._url_detail = url_detail
        self._lyric = lyric
        self._detail = detail
        self._parse()
        
    def _parse(self):
        try:
            # 歌曲 url
            ret = json.loads(self._url_detail)
            self._url = ret['data'][0]['url']
            # 歌词
            lyric = json.loads(self._lyric)
            self._lyric = lyric['lrc']['lyric']
            
            # 详细信息
            detail = json.loads(self._detail)
            song = detail['songs'][0]
            self._name = song['name']
            self._origin_id = song['id']
            self._ar_name = song['ar'][0]['name']
            self._al_name = song['al']['name']
            self._pic_url = song['al']['picUrl']
           
            self._valid = True
        except Exception as ex:
            logger = logging.getLogger(__name__)
            logger.error(ex)
        # url
    
    
    # 歌曲链接[原始信息]
    # _url_detail = ''
    
     # 歌词 [原始信息]
    # _lyric = ''
    
    # 详细信息 [原始信息]
    # _detail = ''

   

