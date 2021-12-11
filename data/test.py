import pygame as pg

pg.init()

mw = pg.display.set_mode((700,700))

pg.mixer.music.load('space.ogg')
pg.mixer.music.play(1)

clock = pg.time.Clock()

while True:

    clock.tick(40)
    pg.display.update()
