import sys
import pygame as pg


CAPTION = "Line/Circle Intersection"
SCREEN_SIZE = (500, 500)
BACKGROUND_COLOR = pg.Color("darkslategrey")


def intersects(rect, r, center):
    circle_distance_x = abs(center[0]-rect.centerx)
    circle_distance_y = abs(center[1]-rect.centery)
    if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
        return False
    if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
        return True
    corner_x = circle_distance_x-rect.w/2.0
    corner_y = circle_distance_y-rect.h/2.0
    corner_distance_sq = corner_x**2.0 +corner_y**2.0
    return corner_distance_sq <= r**2.0


class MoveRect(object):
    def __init__(self):
        self.start = None
        self.stop = None
        self.rect = None

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not self.start:
                self.start = event.pos
            else:
                self.start = None
                self.stop = None
                self.rect = None
        elif event.type == pg.MOUSEMOTION:
            if self.start:
                self.stop = event.pos
                self.rect = self.find_rect()

    def find_rect(self):
        left = min(self.start[0], self.stop[0])
        top = min(self.start[1], self.stop[1])
        width = abs(self.stop[0]-self.start[0])
        height = abs(self.stop[1]-self.start[1])
        return pg.Rect(left, top, width, height)

    def draw(self, surface):
        if self.rect:
            pg.draw.rect(surface, pg.Color("white"), self.rect, 1)


class HitCircle(object):
    def __init__(self, r, center):
        self.r = r
        self.center = center
        self.color = pg.Color("tomato")
        self.hit = False

    def check_hit(self, rect):
        self.hit = intersects(rect, self.r, self.center) if rect else False

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.center, self.r, not self.hit)


class Control(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.done = False
        self.test_rect = MoveRect()
        self.circle = HitCircle(50, (250,250))

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.test_rect.get_event(event)

    def update(self):
        self.circle.check_hit(self.test_rect.rect)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.circle.draw(self.screen)
        self.test_rect.draw(self.screen)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            pg.display.update()
            self.clock.tick(self.FPS)


def main():
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
