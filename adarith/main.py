#!/usr/bin.env python
"""
Ada's world
"""
import os
# from lib.ballgame import BallGame

from arithgame import ArithGame

def main():
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    # game = BallGame(path=main_dir)
    game = ArithGame(path=main_dir)
    game.run()
    



# import sqlalchemy as sa


if __name__ == '__main__':
    main()
    # test_db()

