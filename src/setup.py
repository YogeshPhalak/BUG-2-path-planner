import pygame as pg

pg.init()

# Screen Specification parameters
SCREENSIZE = (1600, 960)
CAPTIONS = "NFZ Path Planner"
BACKGROUND = (0, 100, 0)
BLACK = (0, 0, 0)
BACKALPHA = 255

# Color palette
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (128, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (25, 25, 112)
VIOLET = (138, 43, 226)
PINK = (255, 20, 147)
LINECOLOR = (0, 128, 0)

DISPSURFACE = pg.display.set_mode(SCREENSIZE, pg.SRCALPHA, 32)
pg.display.set_caption(CAPTIONS)

FPS = 30
CLOCK = pg.time.Clock()

NFZ_OFFSET = 30



def background():
    back_surf = pg.Surface(SCREENSIZE)
    back_surf.fill(BACKGROUND)
    back_surf.set_alpha(BACKALPHA)
    DISPSURFACE.blit(back_surf, (0, 0))
    for i in range(0, SCREENSIZE[0], 10):
        pg.draw.line(DISPSURFACE, LINECOLOR, (i, 0), (i, SCREENSIZE[1]), 1)

    for i in range(0, SCREENSIZE[1], 10):
        pg.draw.line(DISPSURFACE, LINECOLOR, (0, i), (SCREENSIZE[0], i), 1)
