from minio import Minio
from io import BytesIO

class MinioClient:
    _bucket_name = "mymusic"

    def __init__(self, endpoint = None, access_key=None, secret_key=None, secure=False) -> None:
        self._db= Minio(endpoint, access_key, secret_key, secure=secure)
    
    def list_bucjets(self):
        print(self._db.list_buckets())
    
    def init_bucket(self):
        if not self._db.bucket_exists(self._bucket_name):
                self._db.make_bucket(self._bucket_name, self._bucket_name)
    
    def insert_a_song(self, name:str, data:bytes):
        self._db.put_object(self._bucket_name, object_name=name, data= BytesIO(data), length=len(data))