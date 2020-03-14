import pygame as pg
from pygame.locals import *

SCREEN_FLAG = pg.RESIZABLE
SCREEN_SIZE = (640, 480)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREE = (0, 255, 0)
BLUE = (0, 0, 255)

BLACK_A = (0, 0, 0, 127)
WHITE_A = (255, 255, 255, 127)
GRAY_A = (127, 127, 127, 127)
RED_A = (255, 0, 0, 127)
GREE_A = (0, 255, 0, 127)
BLUE_A = (0, 0, 255, 127)

BACKGROUND = BLACK



def quit():
    print(f'Good bye')

def init():
    pg.init()
    pg.register_quit(quit)


def draw_text(screen, text='Hello', pos=(0, 0), color=(255, 255, 255), background=(0, 0, 0)):
    font = pg.font.SysFont("Tahoma", 30)
    img = font.render(text, 0, color, background)
    screen.blit(img, pos)

def circle(surface, color=(255, 255, 255), center=(100, 100), radius=100, width=0):
    return pg.draw.circle(surface, color, center, radius, width)

def palette():
    pass

def main():
    init()
    RUNNING = True

    screen = pg.display.set_mode(SCREEN_SIZE, SCREEN_FLAG)
    print(f'Screen: {screen}')

    while RUNNING:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                RUNNING = False
            if event.type == VIDEORESIZE:
                new_size = event.size
                screen = pg.display.set_mode(new_size, SCREEN_FLAG)
    
        rect = pg.display.get_surface().get_rect()

        screen.fill(GRAY)
        draw_text(screen=screen, text=f'Windows: {rect}')

        for r in range(255):
            for g in range(255):
                for b in range(255):
                    circle(screen, (r, g, b), (r+g, b), 0)

        # red_rect = rect.move((-20, 0))
        # circle(screen, RED_A, red_rect.center)
        # # rect.move((-20, 0))

        # gree_rect = rect.move((20, 0))
        # circle(screen, GREE_A, gree_rect.center)
        # rect.move((40, 0))


        pg.display.update() 



if __name__ == '__main__':
    main()