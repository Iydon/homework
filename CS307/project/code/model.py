#!/usr/bin/python3
__all__ = ('User', 'Video', 'User', 'Comment')


import collections
import faker
import math
import os
import requests
import retrying
import time


F = faker.Faker()
Comment = collections.namedtuple('Comments', ('content', 'like', 'user_id', 'timestamp'))


class User:
    '''Bilibili user model

    API:
        - videos: iterator, all Videos
    '''
    def __init__(self, id, info=True):
        self.id = id
        self._headers = {
            'host': 'api.bilibili.com',
            'referer': 'https://www.bilibili.com',
            'user-agent': F.user_agent(),
        }
        if info:
            self.info = self._find_info()

    def __repr__(self):
        return f'<User({self.info["name"]}) @ LV {self.info["level"]}>'

    @property
    def video_ids(self):
        for page in self._videos():
            yield from page

    @property
    def videos(self):
        for page in self._videos():
            for id in page:
                yield Video(id)

    @retrying.retry(stop_max_attempt_number=3)
    def _videos(self, ps=30):
        first_page = self._videos_data_at(1)
        page_info = first_page['data']['page']
        page_number = math.ceil(page_info['count']/ps)
        f, g = self._find_videos, self._videos_data_at
        return (f(g(page+1)) for page in range(page_number))

    def _videos_data_at(self, page, ps=30):
        url = 'https://api.bilibili.com/x/space/arc/search'
        params = dict(mid=self.id, ps=ps, pn=page, order='pubdate')
        response = requests.get(url, params=params, headers=self._headers)
        return response.json()

    def _find_videos(self, data):
        for video in data['data']['list']['vlist']:
            yield video['aid']

    def _find_info(self):
        info = dict()
        # account info
        params = dict(mid=self.id, jsonp='jsonp')
        url = 'https://api.bilibili.com/x/space/acc/info'
        response = requests.get(url, params=params, headers=self._headers)
        data = response.json().get('data')
        for key in ('name', 'sex', 'face', 'sign', 'level', 'birthday'):
            info[key] = data.get(key)
        # up status
        url = 'https://api.bilibili.com/x/space/upstat'
        response = requests.get(url, params=params, headers=self._headers)
        data = response.json().get('data')
        info['archive_view'] = data.get('archive').get('view')
        info['article_view'] = data.get('article').get('view')
        info['likes'] = data.get('likes')
        # relation status
        params = dict(vmid=self.id, jsonp='jsonp')
        url = 'https://api.bilibili.com/x/relation/stat'
        response = requests.get(url, params=params)
        data = response.json().get('data')
        info['following'] = data.get('following')
        info['follower'] = data.get('follower')
        # return value
        return info


class Video:
    '''Bilibili video model

    API:
        - comments, iterator, info of all comments
    '''
    def __init__(self, id, info=True):
        self.id = id
        self._headers = {
            'host': 'api.bilibili.com',
            'referer': 'https://www.bilibili.com',
            'user-agent': F.user_agent(),
        }
        self._timestamp = int(1000*time.time())
        if info:
            self.info = self._find_info()

    def __repr__(self):
        return f'<Video({self.info["title"]}) @ View {self.info["view"]}>'

    @property
    def comments(self):
        '''
        Format:
            - (content, like, user_id, timestamp)
        '''
        for page in self._comments(): 
            yield from page

    @retrying.retry(stop_max_attempt_number=3)
    def _comments(self):
        first_page = self._comments_data_at(1)
        if first_page['data']:
            page_info = first_page['data']['page']
            page_number = math.ceil(page_info['count']/page_info['size'])
            f, g = self._find_comments, self._comments_data_at
            return (f(g(page+1)['data']['replies'])
                for page in range(page_number))
        return [[]]

    def _comments_data_at(self, page, root=0, ps=10, sort=2):
        url = 'https://api.bilibili.com/x/v2/reply'
        params = dict(pn=page, type=1, oid=self.id, sort=sort, _=self._timestamp)
        if root:
            url += '/reply'
            params.update(dict(root=root, ps=ps))
        return requests.get(url, params=params, headers=self._headers).json()

    def _find_comments(self, replies, ps=10):
        if replies:
            for reply in replies:
                message = reply['content']['message']
                mid = reply['member']['mid']
                ctime = reply['ctime']
                like = reply['like']
                yield Comment(message, like, mid, ctime)
                rcount = reply['rcount']
                if rcount:
                    for page in range(math.ceil(rcount/ps)):
                        rpid = reply['rpid']
                        data = self._comments_data_at(page+1, rpid, ps)
                        replies = data['data']['replies']
                        yield from self._find_comments(replies)

    def _find_info(self):
        info = dict()
        # video info
        url = 'https://api.bilibili.com/x/web-interface/view'
        response = requests.get(url, params=dict(aid=self.id))
        data = response.json().get('data')
        for key in ('pic', 'title', 'pubdate', 'desc', 'duration'):
            info[key] = data.get(key)
        info['owner'] = data['owner']['mid']
        # stat info
        stat = data['stat']
        for key in ('view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like'):
            info[key] = stat.get(key)
        return info


if __name__ == '__main__':
    u = User(546195)
    vs = u.videos
    print(next(vs))

    v = Video(70885948)
    cs = v.comments
    print(next(cs))
