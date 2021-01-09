'''单独调用
'''
from api.appannie import Appannie, API
from api.cache import Cache
from models import Config


config = Config()
api = API(**config['appannie'])
cache = Cache(**config['cache'])

help(api.appannie.download_revenue)
print(cache.getsize()/1024/1024)
