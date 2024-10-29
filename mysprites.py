#This file was created by: Umar Khan
player_speed=1.75
#imports all the libraries for the game and data from 'settings'
from typing import Any
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import *
from random import randint
vec=pg.math.Vector2
from main import *
from utilities import *

# create the player class with a superclass of Sprite. Also, initializes and puts it in a group of all_sprites which can be accessed in other classes.
class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(Red)
        # self.rect.x = x
        # self.rect.y = y
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        # self.vx, self.vy = 0, 0
        self.coins = 0
        self.jump_power = 25
        self.jumping = False

        self.speed = player_speed
        #self.vx, self.vy = 0, 0
    #uses the typing library to collect input data from keyboard and make decisions based on it
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.acc.x = -self.speed
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.acc.x = self.speed
        if keys[pg.K_SPACE]:
            self.jump()
        #if keys[pg.K_r]:
           # Game.reset_Player(self)
    def jump(self):
        print('trying to jump...')
        print(self.vel.y)
        self.rect.y +=2
        hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
        self.rect.y -=2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print("still trying to jump")
        
        #creates the collision mechanic to check whether certain sprites are touching each other. This can later be used to create interactions
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                #we added y collision
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    def collide_with_mobs(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
            if hits:
                if self.pos.x > 0:
                    self.game.next_stage("lvl2.txt")
                if self.pos.x < 0:
                    self.game.next_stage("lvl2.txt")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
            if hits:
                if self.pos.y > 0:
                    self.game.next_stage("lvl2.txt")
                if self.pos.y < 0:
                    self.game.next_stage("lvl2.txt")
    def collide_with_stuff(self,group,kill):
        hits=pg.sprite.spritecollide(self,group,kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Speed":
                self.speed+=5
                print("Speed Boost!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("You got a Coin!")
                self.coins+=1
            if str(hits[0].__class__.__name__) == "Jump":
                print("Jump Boost!")
                self.jump_power+=5
                #add a timer
                self.jump_power-=5
                

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        # reverse order to fix collision issues
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_mobs(self.game.all_mobs)
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.collide_with_mobs('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_mobs('y')
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_mobs(self.game.all_mobs)
        if quit == True:
            print("Quiter")
# added Mob - moving objects
#is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        #color of the mob is being set to green
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.game=game
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #the speed of the Mob is set to 30
        self.speed = 25
        #create if statement to make the Mobs bounce back when they hit the wall
    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        #if the x value is greater or less than either side of the screen
        if self.rect.x > WIDTH or self.rect.x < 0:
            #then reverse the speed by doing *= -1 and move the Mob down by 32
            self.speed *= -1
            # self.rect.y += 32
            # print("I am on the side of the screen")
        #checks for if the y value of the Mob is greater than the height of the screen
        if self.rect.y > HEIGHT:
            #if it is then set the y-value to 0
            self.rect.y = 0
            # print("I am on the bottom of the screen")
            

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.game=game
        self.image.fill(Blue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    def update(self):
        pass
class Speed(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.game=game
        self.image.fill(Orange)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass
class Jump(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.game=game
        self.image.fill(Purple)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.game=game
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass