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
    for file in tqdm.tqdm(os.listdir(comment_path)):
        with open(os.path.join(comment_path, file), 'r') as fc:
            for user_id in json.load(fc):
                if not os.path.exists(f(user_id)):
                    with open(f(user_id), 'w') as fu:
                        json.dump(User(user_id).info, fu, ensure_ascii=False)


def convert_to_database():
    f = lambda p: os.path.join(user_path, p)
    g = lambda p: os.path.join(comment_path, p)
    h = lambda p: os.path.join(video_path, p)

    print('User loaing...')
    for file in tqdm.tqdm(os.listdir(user_path)):
        id = file.replace('.json', '')
        with open(f(file), 'r') as fr:
            data = json.load(fr)
            del data['face'], data['birthday']
            session.add(UserDB(id=int(id), **data))
    print('Video loaing...')
    for file in tqdm.tqdm(os.listdir(video_path)):
        id = file.replace('av', '').replace('.json', '')
        with open(h(file), 'r') as fr:
            data = json.load(fr)
            del data['pic'], data['owner']
            session.add(VideoDB(id=int(id), **data))
    print('Comment loading...')
    for file in tqdm.tqdm(os.listdir(comment_path)):
        id = file.replace('av', '').replace('.json', '')
        with open(g(file), 'r') as fr:
            data = json.load(fr)
            for user_id , comments in data.items():
                for time, content in comments.items():
                    c = CommentDB(
                        user_id=int(user_id), video_id=int(id),
                        pubdate=int(time), content=content,
                    )
                    session.add(c)
            break
    print('Finished...')
    session.commit()
    session.close()


if __name__ == '__main__':
    commands = dict(
        collect_bilibili_data=collect_bilibili_data,
        convert_to_database=convert_to_database,
    )
    fire.Fire(commands)
