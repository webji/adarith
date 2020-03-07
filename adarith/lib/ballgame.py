#!/usr/bin/env python

"""
A basket ball game
"""


VERSION = '0.1'

try:
    import sys, random, math, os, getopt
    import pygame
    from socket import *
    from pygame.locals import *

    from .game import GameBase
    from .basketball import BasketBall
    from .bat import Bat
except ImportError as e:
    print(f'Failed to load module: {e}')
    sys.exit(2)




class BallGame(GameBase):
    
    
    def _init_players(self):
        bat_path = os.path.join(self.res_dir, 'bat_100_100.png')  
        self.player1 = Bat(path=bat_path, side='left')
        self.player2 = Bat(path=bat_path, side='right')
        

    def _init_atlas(self):
        ball_path = os.path.join(self.res_dir, 'basketball_50_50.png')  
        speed = 13
        rand = ((0.1 * (random.randint(5, 8))))
        vector = (0.47, speed)
        self.ball = BasketBall(path=ball_path, vector=vector)


    def _init_sprites(self):
        self.playerssprites = pygame.sprite.RenderPlain((self.player1, self.player2))
        self.ballsprite = pygame.sprite.RenderPlain(self.ball)


    def _handle_event(self, event=None):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.player1.move_up()
            if event.key == K_z:
                self.player1.move_down()
            if event.key == K_UP:
                self.player2.move_up()
            if event.key == K_DOWN:
                self.player2.move_down()
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_z:
                self.player1.movepos = [0, 0]
                self.player1.state = 'still'
            if event.key == K_UP or event.key == K_DOWN:
                self.player2.movepos = [0, 0]
                self.player2.state = 'still'

        return super().handle_event(event=event)


    def _update_screen(self):
        self.screen.blit(self.background, self.ball.rect, self.ball.rect)
        self.screen.blit(self.background, self.player1.rect, self.player1.rect)
        self.screen.blit(self.background, self.player2.rect, self.player2.rect)

        self.ballsprite.update(self.player1, self.player2)
        self.playerssprites.update()

        self.ballsprite.draw(self.screen)
        self.playerssprites.draw(self.screen)
        return super().update_screen()


    def _pre_quit(self, **kwargs):
        print('Goodby Ada')
        return super().pre_quit(**kwargs)
        

    