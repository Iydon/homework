import sys
sys.path.append('..')

import timeit
from sqlalchemy.sql import func

from database import session, Video, Comment


def sql_statement(statements, attemp_number=3):
    result = dict()
    for statement in statements:
        result[statement] = timeit.timeit(statement, number=attemp_number, globals=globals())
    return result


if __name__ == '__main__':
    statements = (
        'session.query(Video).filter(Video.title.like("%燃%")).all()',
        'session.query(Comment).filter(Comment.content.like("%自制%")).all()',
        'session.query(Video, Comment).join(Comment).limit(65536).all()',
        'session.query(func.max(func.length(Comment.content))).scalar()',
        'session.query(Video.user_id, func.count("*").label("cnt")).group_by(Video.user_id).all()'
    )
    # select * from Video as v where v.title like "%燃%";
    # select * from Comment as c where c.content like "%自制%";
    # select * from Video as v join Comment as c on v.id = c.video_id limit 65536;
    # pass
    # pass
    result = sql_statement(statements)
    print(result)
