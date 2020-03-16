#!/usr/bin/python3
__all__ = ('session', 'User', 'Video', 'Comment')


from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import database_path


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    videos = relationship('Video', back_populates='user')
    comments = relationship('Comment', back_populates='user')

    name = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    sign = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    archive_view = Column(Integer, nullable=False)
    article_view = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    following = Column(Integer, nullable=False)
    follower = Column(Integer, nullable=False)


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='videos')
    comments = relationship('Comment', back_populates='video')

    title = Column(String, nullable=False)
    pubdate = Column(Integer, nullable=False)
    desc = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    view = Column(Integer, nullable=False)
    danmaku = Column(Integer, nullable=False)
    reply = Column(Integer, nullable=False)
    favorite = Column(Integer, nullable=False)
    coin = Column(Integer, nullable=False)
    share = Column(Integer, nullable=False)
    like = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='comments')
    video_id = Column(Integer, ForeignKey('video.id'))
    video = relationship('Video', back_populates='comments')

    pubdate = Column(Integer, nullable=False)
    content = Column(String, nullable=False)


engine = create_engine(database_path)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


if __name__ == '__main__':
    '''
    session.add(...)
    session.commit()
    session.close()

    print(session.query(...).all())
    print(session.query(...).filter(...).first())
    '''
    u = User(
        id=8888, name='XXXX', sex='保密', sign='hello world',
        level=5, archive_view=100, article_view=100,
        likes=100, following=100, follower=100,
    )
    v = Video(
        id=1024, user_id=8888, title='测试标题', pubdate=1496979918,
        desc='懒', duration=233, view=100, danmaku=100, reply=100,
        favorite=100, coin=100, share=100, like=100,
    )
    c = Comment(
        user_id=8888, video_id=1024, pubdate=1496979888, content='前排',
    )
