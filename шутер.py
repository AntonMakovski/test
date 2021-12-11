from typing import Mapping
from pygame.constants import HIDDEN, K_LEFT, K_RIGHT, K_SPACE, MOUSEBUTTONDOWN
import pygame as pg
import random
import data
import time

global lose
global winn

def rezults(font, winn, lose):
    if not(lose):
        rezult=font.render('there is a winner', True, (100,200,100))
    else:
        rezult=font.render('you lose', True, (200,100,100))
    mw.blit(rezult,(350, 250))
def game(variors, bulets, i):
    global out
    global cicked
    global lose 
    
    if i%60 == 0:
        if len(variors) < 5:
            for i in range(5-len(variors)):
                objekt = Enemy(data.ufo_image_path)
                variors.append(objekt)

        for i in range(3-len(meteors)):
            met = Asteroid(2)
            meteors.append(met)

    for element in variors:
        if element.rect.y > 500:
            variors.remove(element)
            out += 1
        elif element.collised_rocket(rocket.rect):
            variors.remove(element)
            rocket.hels -= 1 
  
        for bulet in bulets:
            if element.collised_bullet(bulet):
                variors.remove(element)
                bulets.remove(bulet)
                cicked += 1
                break

            if bulet.rect.y ==  0:
                bulets.remove(bulet)

            
            if len(bulets) > 0:    
                bulet.go()
  
        element.go()
    for meteor in meteors:
            meteor.go()
            if meteor.rect.y>500:
                meteors.remove(meteor)
            if meteor.colide_rocket(rocket):
                rocket.hels -= 1
                meteors.remove(meteor)
                print(rocket.hels)
    
    if rocket.hels == 0:
        lose = True 

pg.init()

mw = pg.display.set_mode((700,500))
pg.mixer.music.load(data.audio_path)  
background = pg.image.load(data.background_image_path).convert_alpha()

variors = list()
bulets = list()
meteors = list()


class Game_while():
    def __init__(self, FPS):
        self.FPS = FPS

        self.menu_work = False

        self.efects_volume = 0.5

        self.i = 0

    def working(self, out, cicked):
        global lose
        global winn
        for event in pg.event.get():
            if event.type == pg.QUIT :
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.menu_work == False:    
                        self.menu_work = True
                    else:
                        self.menu_work = False

            rocket.geting(event)
            menu.getting(event)

        if self.menu_work:
            self.efects_volume = menu.working()

        if self.menu_work == False and not(lose) and not(winn):
            game(variors, bulets, self.i)
            
            rocket.do_somesing(self.efects_volume, self.i)
        if lose or winn:
            rezults(pg.font.Font(None, 70), winn, lose)
        
       
        self.i += 1

        clock.tick(self.FPS)

class Plaer():
    def __init__(self, x, y, width, hight, image, sound):
        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(),(width,hight))

        self.wight = width
        self.hight = hight

        self.fire_sound = pg.mixer.Sound(sound)

        self.rect = pg.rect.Rect(x,y,self.wight,self.hight)

        self.bullets = 5
        
        self.hels = 5

        self.re_time = 0
        #flags
        self.left = False
        self.right = False
        self.do_fire = False
        self.re_bul = False

    def geting(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                self.left = True
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                self.right = True
            
            elif event.key == pg.K_SPACE:
                self.do_fire = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                self.left = False
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                self.right = False
            
            elif event.key == pg.K_SPACE:
                self.do_fire = False        

    def fire(self, x, i, volume):
        if i % 4 == 0:
            if self.bullets > 0:    
                bulets.append(Bullet(data.bullet_image_path, x))

                self.fire_sound.set_volume(volume)
                self.fire_sound.play(1)

                if self.bullets == 1:
                    self.re_bul = True
                    self.re_time = time.time()
                self.bullets -= 1
                

    def do_somesing(self, volume, i):
        if self.re_bul:
            if (self.re_time-time.time())<=-3:
                self.bullets+=5
                self.re_bul = False

        if self.rect.x > 0:
            if self.left:
                self.rect.x -= 5
        if self.rect.x < 590:
            if self.right:
                self.rect.x += 5
        
        if self.do_fire:    
            self.fire(self.rect.x, i, volume)

        mw.blit(self.image,(self.rect.x, self.rect.y))
    
class Enemy():
    def __init__(self, image):
        self.width = 122
        self.hight = 65

        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(), (self.width,self.hight))

        self.x = random.randint(0,578)
        self.y = 0

        self.rect = pg.rect.Rect(self.x, self.y, self.width, self.hight)

    def go (self):
        self.rect.y += 1

        mw.blit(self.image, (self.rect.x, self.rect.y)) 
    
    def collised_rocket(self, object):
        return self.rect.colliderect(object)

    def collised_bullet(self, object):
        return self.rect.colliderect(object) 

class Bullet():
    def __init__(self, image, guns_x):
        self.width = 16
        self.hight = 32
        self.x = guns_x + 47
        self.y = 308
        
        self.rect = pg.rect.Rect(self.x, self.y, self.width, self.hight)
        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(), (self.width,self.hight))
    
    def go(self):
        self.rect.y -= 2
        mw.blit(self.image, (self.rect.x, self.rect.y)) 

class Asteroid():
    def __init__(self, speed):
        self.image = pg.transform.scale(pg.image.load(data.asteroid_image_path).convert_alpha(), (100,100))
        self.speed = speed

        self.x = random.randint(0, 300)
        self.y = 0

        self.rect = pg.rect.Rect(self.x, self.y, 100,100)

    def go(self):
        self.rect.y += self.speed 
        mw.blit(self.image, (self.rect.x,self.rect.y))

    def colide_rocket(self, racket):
        if self.rect.colliderect(rocket.rect):
            return True

class Menu():
    def __init__(self, width1, width2):
        self.main_surface = pg.Surface((600,400))
        self.main_surface.fill((20,20,40))

        self.volume_rect1 = pg.rect.Rect(200, 170, 200, 20)
        self.seting_rect1 = pg.rect.Rect(200, 170, 100, 20)

        self.volume_rect2 = pg.rect.Rect(200, 210, 200, 20)
        self.seting_rect2 = pg.rect.Rect(200, 210, 100, 20)

        self.font = pg.font.Font(None, 70)

        self.text1 = self.font.render('Музыка', True, (0,0,0))
        self.text2 = self.font.render('Эффекты', True, (0,0,0))

        self.button_presed = False

        self.volume_music = 0.5
        self.volume_efects = 0.25

    def getting(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_presed = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.button_presed = False

    def working(self):
        mw.blit(self.main_surface, (50,50))

        self.main_surface.blit(self.text1, (200,120))
        pg.draw.rect(self.main_surface, (255,255,255), self.volume_rect1)
        pg.draw.rect(self.main_surface, (255,255,255), self.volume_rect2)

        self.main_surface.blit(self.text2, (180, 230))
        pg.draw.rect(self.main_surface, (200,100,100), self.seting_rect2)
        pg.draw.rect(self.main_surface, (200,100,100), self.seting_rect1)
        

        self.cursor_pos_x, self.cursor_pos_y = pg.mouse.get_pos()

        self.cursor_pos_x -= 250
        self.cursor_pos_y -= 220

        if self.button_presed:    
            if self.cursor_pos_x >= 0 and self.cursor_pos_x <= 200:
                    if self.cursor_pos_y >= 0 and self.cursor_pos_y <= 20:
                        self.seting_rect1.width = self.cursor_pos_x
                        
                        self.volume_music = self.seting_rect1.width/200

                    elif self.cursor_pos_y >= 40 and self.cursor_pos_y <= 60:
                        self.seting_rect2.width = self.cursor_pos_x

                        self.volume_efects = self.seting_rect2.width/200

        pg.mixer.music.set_volume(self.volume_music)

        return self.volume_efects

class Text():
    def __init__(self):
        self.font = pg.font.Font(None, 70)

        global out
        global cicked

        self.text_out = self.font.render(('Пропущено '+str(out)), True, (255,255,255))
        self.text_cicked = self.font.render(('Убито '+str(cicked)), True, (255,255,255))
    
    def render(self):
        self.text_out = self.font.render(('Пропущено '+str(out)), True, (255,255,255))
        self.text_cicked = self.font.render(('Убито '+str(cicked)), True, (255,255,255))

        mw.blit(self.text_out,(0,0))
        mw.blit(self.text_cicked,(0,50))

out = 0
cicked = 0

lose = False
winn = False

text = Text()
gameWhile = Game_while(60)
rocket = Plaer(300, 340, 110, 160, data.rocket_image_path, data.fire_sound_path)
menu = Menu(100,100)

pg.mixer.music.play(-1)

clock = pg.time.Clock()

while True:
    mw.blit(background, (0,0))

    gameWhile.working(out, cicked)
    text.render()
    pg.display.update()  
