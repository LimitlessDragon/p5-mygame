#This file was created by: Umar Khan
player_speed=10
#imports all the libraries for the game and data from 'settings'
from typing import Any
import pygame as pg
from pygame.sprite import Group, Sprite
from settings import *
from random import randint

# create the player class with a superclass of Sprite. Also, initializes and puts it in a group of all_sprites which can be accessed in other classes.
class Player(Sprite):        
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = player_speed
        self.vx, self.vy = 0, 0
        self.coins=0

    #uses the typing library to collect input data from keyboard and make decisions based on it
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed
        if keys[pg.K_a]:
            self.vx -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
    #creates the collision mechanic to check whether certain sprites are touching each other. This can later be used to create interactions
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.x > 0:
                    self.x = hits[0].rect.left - TILESIZE
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
                #we added y collision
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_stuff(self,group,kill):
        hits=pg.sprite.spritecollide(self,group,kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Speed":
                self.speed+=5
                print("Steroids!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("You got a Coin!")
                self.coins+=1

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # Teleportation: if the x.rect is equal to the Width
        if self.rect.x > WIDTH:
                self.x = 0
        elif self.rect.x < 0:
            self.x = WIDTH - TILESIZE
        if self.rect.y > HEIGHT:
                self.y = 0
        elif self.rect.y < 0:
            self.y = HEIGHT - TILESIZE

        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
# added Mob - moving objects
#is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
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
        self.speed = 20
        #create if statement to make the Mobs bounce back when they hit the wall
    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        #if the x value is greater or less than either side of the screen
        if self.rect.x > WIDTH or self.rect.x < 0:
            #then reverse the speed by doing *= -1 and move the Mob down by 32
            self.speed *= -1
            self.rect.y += 32
            # print("I am on the side of the screen")
        #checks for if the y value of the Mob is greater than the height of the screen
        if self.rect.y > HEIGHT:
            #if it is then set the y-value to 0
            self.rect.y = 0
            # print("I am on the bottom of the screen")
        if self.rect.colliderect(self.game.player):
            #player's controls get inverted
            #self.game.player.speed*=-1
            #mob goes backwards
            self.speed*=-1
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