
from http import server
from selenium.webdriver.support.wait import WebDriverWait
from browsermobproxy import Server as ProxyServer
from browsermobproxy import Client as ProxyClient
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as cond
import time
from .song_info import SongInfo
from enum import IntEnum

obj = {}

class SearchType(IntEnum):
    BySong=1
    ByAr=100
    ByAl=10

# def new_proxyClient(path):
#     server = ProxyServer(path)
#     return server.create_proxy()

# def new_edgeDriver(path, proxy_cli:ProxyClient)->WebDriver:
#     from selenium.webdriver.edge import service
#     from selenium.webdriver.edge.options import Options

#     driver_options = Options()
#     driver_options.add_argument('--ignore-certificate-errors')
#     driver_options.add_argument('--disable-gpu')
#     driver_options.add_argument('--headless')
#     driver_options.add_argument('--proxy-server={0}'.format(proxy_cli.proxy))
#     driver_service = service.Service(path)
#     driver = webdriver.Edge(service=driver_service, options=driver_options)    
#     return driver

class ProxyAndDriver:
    def __init__(self, proxy_path:str, dirver_path:str) -> None:
        """proxy_path"""
        self.proxy_server_ = ProxyServer(proxy_path)
        self.proxy_server_.start()
        self.dirver_path_ = dirver_path
    
    def getEdgeDriver(self):
        from selenium.webdriver.edge import service
        from selenium.webdriver.edge.options import Options

        proxy_cli = self.proxy_server_.create_proxy()
        driver_options = Options()
        driver_options.add_argument('--ignore-certificate-errors')
        driver_options.add_argument('--disable-gpu')
        driver_options.add_argument('--headless')
        driver_options.add_argument('--proxy-server={0}'.format(proxy_cli.proxy))
        driver_service = service.Service(self.dirver_path_)
        driver = webdriver.Edge(service=driver_service, options=driver_options)    
        return (proxy_cli,driver)  
     
    def stop(self):
        self.proxy_server_.stop()

        
    
class NetEase:
    def __init__(self, cli:ProxyClient, driver:WebDriver)-> None:
        self.proxy_client_ = cli
        self.driver_ = driver

    def search(self, key:str, type:SearchType = SearchType.BySong):
        
        url = 'https://music.163.com/#/search/m/?s={}&type={}'.format(key, type)
        # cls.initEnv()
        try:
            wait = WebDriverWait(self.driver_, 5)
            
            self.proxy_client_.new_har(options={
                'captureContent': True,
                'captureHeaders': True,
            })
            
            self.driver_.get(url)
            wait.until(cond.frame_to_be_available_and_switch_to_it(
                (By.ID, "g_iframe")), '切换frame失败')
            
            result_ = self.proxy_client_.har
            
            for entry in result_['log']['entries']:
                request = entry['request']
                response = entry['response']
                req_url:str = request['url']
                if req_url.endswith('web?csrf_token='):
                    songs = response['content']['text']
                    return songs
            return None
        finally:
            self.driver_.close()
    
    def query_song_info(self, song_id:str):
        try:
            wait = WebDriverWait(self.driver_, 5)

            url = 'https://music.163.com/#/song?id={}'.format(song_id)
            
            self.driver_.get(url)
                        
            wait.until(cond.frame_to_be_available_and_switch_to_it(
                (By.ID, "g_iframe")), '切换frame失败')

            self.proxy_client_.new_har(options={
                'captureContent': True,
                'captureHeaders': True,
            })
            self.driver_.find_element(By.CSS_SELECTOR, value='a[title="播放"]').click()
            
            time.sleep(2)
            result_ = self.proxy_client_.har

            url_detail =''
            lyric = ''
            detail = ''
            for entry in result_['log']['entries']:
                request = entry['request']
                response = entry['response']
                req_url:str = request['url']
                if  req_url.endswith('v1?csrf_token='):
                    url_detail = response['content']['text']
                    
                if req_url.endswith('lyric?csrf_token='):
                    lyric = response['content']['text']
                    
                if req_url.endswith('detail?csrf_token='):
                    detail = response['content']['text']

            return SongInfo(url_detail, lyric, detail)
        except Exception as ex:
            return None
        finally:
            self.driver_.close()