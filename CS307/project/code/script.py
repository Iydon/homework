#!/usr/bin/python3
import collections
import fire
import json
import os
import tqdm

from config import user_ids, comment_path, user_path, video_path
from database import session
from database import User as UserDB, Video as VideoDB, Comment as CommentDB
from model import User, Video
from config import string_max_len


def collect_bilibili_data():
    f = lambda i: os.path.join(user_path, f'{i}.json')
    g = lambda i: os.path.join(comment_path, f'av{i}.json')
    h = lambda i: os.path.join(video_path, f'av{i}.json')

    for user_id in tqdm.tqdm(user_ids):
        user = User(user_id)
        with open(f(user_id), 'w') as fu:
            json.dump(user.info, fu, ensure_ascii=False)
        for video in user.videos:
            if not os.path.exists(g(video.id)):
                comments = collections.defaultdict(dict)
                for comment in video.comments:
                    content, _, user_id, time = comment
                    comments[user_id][time] = content
                with open(g(video.id), 'w') as fv:
                    json.dump(comments, fv, ensure_ascii=False)
            if not os.path.exists(h(video.id)):
                with open(h(video.id), 'w') as fv:
                    json.dump(video.info, fv)
    result = set()
    for file in tqdm.tqdm(os.listdir(comment_path)):
        with open(os.path.join(comment_path, file), 'r') as fc:
            for user_id in json.load(fc):
                result.add(user_id)
    with open(os.path.join(user_path, 'others.json'), 'w') as fu:
        json.dump(list(result), fu)


def drop_database():
    from database import Base, engine

    Base.metadata.drop_all(engine)


def convert_to_database(group=100000):
    f = lambda p: os.path.join(user_path, p)
    g = lambda p: os.path.join(comment_path, p)
    h = lambda p: os.path.join(video_path, p)
    count = 0

    print('User loaing...')
    with open(f('others.json'), 'r') as fr:
        users = json.load(fr)
        for user_id in tqdm.tqdm(users):
            session.add(UserDB(id=int(user_id)))
            count += 1
            if count%group == 0:
                session.commit()
    for file in tqdm.tqdm(os.listdir(user_path)):
        if file == 'others.json':
            continue
        id = file.replace('.json', '')
        if id not in users:
            session.add(UserDB(id=int(id)))
            session.commit()
            count += 1
            if count%group == 0:
                session.commit()
    for file in tqdm.tqdm(os.listdir(user_path)):
        if file == 'others.json':
            continue
        id = file.replace('.json', '')
        if id not in users:
            if not session.query(UserDB).filter(UserDB.id==int(id)).count():
                session.add(UserDB(id=int(id)))
                session.commit()
    print('Video loaing...')
    for file in tqdm.tqdm(os.listdir(video_path)):
        id = file.replace('av', '').replace('.json', '')
        with open(h(file), 'r') as fr:
            data = json.load(fr)
            data['user_id'] = data['owner']
            if len(data['desc']) > string_max_len:
                data['desc'] = data['desc'][:string_max_len]
            del data['pic'], data['owner']
            user_id = data['user_id']
            if str(user_id) not in users:
                users.append(str(user_id))
                if not session.query(UserDB).filter(UserDB.id==user_id).count():
                    session.add(UserDB(id=user_id))
                    session.commit()
            session.add(VideoDB(id=int(id), **data))
            count += 1
            if count%group == 0:
                session.commit()
    session.commit()
    print('Comment loading...')
    for file in tqdm.tqdm(os.listdir(comment_path)):
        if not os.path.exists(os.path.join(video_path, file)):
            continue
        id = file.replace('av', '').replace('.json', '')
        with open(g(file), 'r') as fr:
            data = json.load(fr)
            result = [None] * sum(map(len, data.values()))
            ith = 0
            for user_id , comments in data.items():
                for time, content in comments.items():
                    if len(content) > string_max_len:
                        content = content[:string_max_len]
                    result[ith] = CommentDB(
                        user_id=int(user_id), video_id=int(id),
                        pubdate=int(time), content=content,
                    )
                    ith += 1
            session.bulk_save_objects(result) # more faster
            session.commit()
    print('Finished...')
    session.close()


def convert_to_database_with_bulk(users, videos, comments, number=100000):
    '''Perform a bulk save of the given iterations

    Argument:
        - users: Iterable
        - videos: Iterable
        - comments: Iterable
        - number: int, number of elements

    References:
        - https://stackoverflow.com/questions/3659142/bulk-insert-with-sqlalchemy-orm
        - https://tutorials.technology/tutorials/Fast-bulk-insert-with-sqlalchemy.html
    '''
    # raise NotImplementedError

    def split(its, number):
        result = [None] * number
        ith = 0
        for ele in its:
            result[ith] = ele
            if (ith+1)%number == 0:
                yield result
                ith = 0
            ith += 1
        yield tuple(filter(bool, result))

    for groups in (users, videos, comments):
        for group in split(groups, number):
            session.bulk_save_objects(group)
            session.commit()


if __name__ == '__main__':
    commands = dict(
        collect_bilibili_data=collect_bilibili_data,
        drop_database=drop_database,
        convert_to_database=convert_to_database,
        convert_to_database_with_bulk=convert_to_database_with_bulk,
    )
    fire.Fire(commands)
