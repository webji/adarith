#!/usr/bin.env python
"""
Ada's world
"""
import os
# from lib.ballgame import BallGame

from lib.arithgame import ArithGame

def main():
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    # game = BallGame(path=main_dir)
    game = ArithGame(path=main_dir)
    game.run()
    



import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from model import Base
from model.user_model import UserModel
from model.setting_model import SettingModel
from model.question_model import QuestionModel

def test_db():
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    db_engine = sa.create_engine(f'sqlite:///{os.path.join(main_dir, "data/adarith.db?check_same_hread=False")}', echo=True)
    Base.metadata.create_all(db_engine)
    db_session = sessionmaker(bind=db_engine)
    db_session = db_session()
    
    User.init_user(db_session)
    Setting.init_setting(db_session)
    Question.init_question(db_session)

if __name__ == '__main__':
    main()
    # test_db()

