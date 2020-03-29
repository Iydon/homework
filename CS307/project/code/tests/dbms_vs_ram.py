import sys
sys.path.append('..')

import collections
import json
import os
import timeit
import tqdm

from config import video_path
from database import session, Video
from util import sizeof


keys = ('pic', 'title', 'pubdate', 'desc', 'duration', 'owner',
    'view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like')


def load_json_into_ram(display=False):
    result = dict()
    Video = collections.namedtuple('Video', keys)
    for file in (tqdm.tqdm if display else iter)(os.listdir(video_path)):
        video_id = int(file.replace('av', '').replace('.json', ''))
        with open(os.path.join(video_path, file)) as f:
            data = json.load(f)
            result[video_id] = Video(*(data[key] for key in keys))
    return result


def load_csv_into_ram():
    Video = collections.namedtuple('Video', keys)
    with open('videos.csv', 'r') as f:
        for line in f.readlines():
            try:
                yield Video(*line.strip().strip('"').split('","'))
            except:
                continue


def test_title_contains(session, videos, substrs, attempt_number=5):
    '''ORM, SQL, RAM
    '''
    result = dict(ORM=dict(), SQL=dict(), RAM=dict())
    sql = 'select * from public.video as v where v.title like :p;'
    stmt_1 = 'session.query(Video).filter(Video.title.like("%{}%")).all()'
    stmt_2 = 'session.execute({}, {}).fetchall()'
    stmt_3 = '[video for video in videos.values() if {} in video.title]'
    f = lambda stmt: timeit.timeit(stmt, number=attempt_number, globals=globals())
    for substr in substrs:
        result['ORM'][substr] = f(stmt_1.format(substr))
        result['SQL'][substr] = f(stmt_2.format(repr(sql), dict(p=repr(substr))))
        result['RAM'][substr] = f(stmt_3.format(repr(substr)))
    return result


if __name__ == '__main__':
    # %run -i __file__
    if 'videos' not in locals():
        videos = load_json_into_ram()
    if 'videos.csv' not in os.listdir():
        with open('videos.csv', 'w') as fw:
             for file in os.listdir(video_path):
                 with open(os.path.join(video_path, file), 'r') as fr:
                     data = json.load(fr)
                     line = '","'.join(str(data[key]) for key in keys)
                     fw.write(f'"{line}"\n')


    print('Size of video:', sizeof(videos))

    keywords = ('震惊', '内幕', '锤', '抑郁', '盗', '赞')
    result = test_title_contains(session, videos, keywords)
    length = {key: len(tuple(filter(lambda v: key in v.title, videos.values())))
        for key in keywords}
