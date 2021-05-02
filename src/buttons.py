from setup import *
from threading import Timer

BUTTON_PRESSED = (128, 128, 128)
BUTTON_RELEASED = (105, 105, 105)


class Button:
    def __init__(self, x, y, w, h, name, toggle=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.pressed = False
        self.fontObj = pg.font.Font('freesansbold.ttf', 12)
        self.textSurfaceObj = None
        self.textRectObj = None
        self.toggle = toggle

    def mouse_cb(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h:
            self.pressed = not self.pressed
        if self.pressed and self.toggle:
            Timer(0.3, self.reset).start()

    def reset(self):
        self.pressed = False

    def draw(self):
        if self.pressed:
            pg.draw.rect(DISPSURFACE, BUTTON_PRESSED, (self.x, self.y, self.w, self.h))
            self.textSurfaceObj = self.fontObj.render(self.name, True, BLACK, BUTTON_PRESSED)
            self.textRectObj = self.textSurfaceObj.get_rect()
            self.textRectObj.center = (self.x + self.w // 2, self.y + self.h // 2)
            DISPSURFACE.blit(self.textSurfaceObj, self.textRectObj)
        else:
            pg.draw.rect(DISPSURFACE, BUTTON_RELEASED, (self.x, self.y, self.w, self.h))
            self.textSurfaceObj = self.fontObj.render(self.name, True, BLACK, BUTTON_RELEASED)
            self.textRectObj = self.textSurfaceObj.get_rect()
            self.textRectObj.center = (self.x + self.w // 2, self.y + self.h // 2)
            DISPSURFACE.blit(self.textSurfaceObj, self.textRectObj)
