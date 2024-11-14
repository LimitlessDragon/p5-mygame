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
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((32, 32))
        self.image = self.game.player_img
        self.image.set_colorkey(Black)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        self.coins = 0
        self.jump_power = 25
        self.jumping = False
        self.speed = player_speed
        self.invulnerable_cd = Cooldown()
        self.mobs_can_attack = True
        self.mouse_pos = (0,0)
        self.health = 3
        self.mobs_can_attack= True
        self.cd = Cooldown()
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
        if pg.mouse.get_pressed()[0]:
            self.shoot()
    def shoot(self):
        self.cd.event_time = floor(pg.time.get_ticks() / 1000)
        if self.cd.delta > 0.1:
            print(pg.mouse.get_pos())
            print(self.pos)
            self.mouse_pos = pg.mouse.get_pos()
            p=Projectile(self.game, self.rect.x, self.rect.y)
            self.mouse_pos = pg.mouse.get_pos()
            if self.mouse_pos[0] < self.pos.x:
                p.speed *= -1
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
        
        #creates the collision mechanic to check whether walls are touching the Player in which to
        # make sure the Player can't go through walls
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
    # The mob collision system is similar to that of the wall's where from 4 directions it check whether the Player
    # is touching the Mob. If so it switches to the "lvl2.txt" which is the game_over stage using the next_stage
    # function in the self.update() part of main.py
    def collide_with_mobs(self, dir, mobs_can_attack):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
            if hits:
                if self.pos.x > 0 and self.mobs_can_attack == True:
                    self.mob_can_attack = False
                    self.invulnerable_cd.event_time = floor(pg.time.get_ticks()/1000)
                if self.pos.x < 0 and self.mobs_can_attack == True:
                    self.health -=1
                    self.mob_can_attack = False
                    self.invulnerable_cd.event_time = floor(pg.time.get_ticks() / 1000)
                    
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
            if hits:
                if self.pos.y > 0 and self.mobs_can_attack == True:
                    self.health -=1
                    self.mob_can_attack = False
                    self.invulnerable_cd.event_time = floor(pg.time.get_ticks() / 1000)
                if self.pos.y < 0  and self.mobs_can_attack == True:
                    self.health -=1
                    self.mob_can_attack = False
                    self.invulnerable_cd.event_time = floor(pg.time.get_ticks() / 1000)
    # collide_with_stuff creates interactions between the all_powerups groups and can change the speed, jump_power, 
    # it also needs a timer
    def collide_with_stuff(self,group,kill):
        hits=pg.sprite.spritecollide(self,group,kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Speed":
                print("I got one")
                self.speed+=5
            if str(hits[0].__class__.__name__) == "Coin":
                print("You got a Coin!")
                self.coins+=1
            if str(hits[0].__class__.__name__) == "Jump":
                print("Jump Boost!")
                self.jump_power+=5
                print("now time to wait")
            if str(hits[0].__class__.__name__) == "Mob":
                self.health-=1
    # jumping mechanism in which if the player is touching a class from the all_walls group, then
    # it can jump the set jump power (in settings)
    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
    def update(self):
        self.cd.ticking()
        self.invulnerable_cd.ticking()
        if self.invulnerable_cd.delta > 3:
            print("i can get hit again")
            self.mob_can_attack = True
        # if self.mobs_can_attack:
        #     self.collide_with_mobs(self.game.all_powerups, True)
        if self.health < 0:
            self.game.next_stage("lvl2.txt")
            print("The Player's Health: "+str(self.health))
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_mobs(self.game.all_mobs, True)
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.collide_with_mobs('x', True)
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_mobs('y', True)
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_mobs(self.game.all_mobs, True)
# added Mob - moving objects
#is a child class of Sprite
# The Mob is in the group of all_mobs in which above the interactions between Mobs and Players can be created
class Mob(Sprite):
    def __init__(self, game, x, y, health):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        # color of the mob is being set to green
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.game=game
        self.rect.x = x
        self.rect.y = y
        self.health=1
        # if self.game.loading== True:
        #     self.health = 2
        #     print("The Armor is Twice as thick now! MuhahahaHAHA!")
        # Each Mob is the size of 32 by 32 pixels or 1 TILESIZE ( in settings)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #the speed of the Mob is set to 30
        self.speed = 25
        #create if statement to make the Mobs bounce back when they hit the wall
    # this method updates the Mob sprite so that it is always checking whether it is touching the side of the
    # screen, so it can go backwards using an if statement.
    def collide_with_projectile(self,group,kill, health):
            hits=pg.sprite.spritecollide(self,group,kill)
            if hits:
                if str(hits[0].__class__.__name__) == "Projectile":
                    self.health -= 1
                if self.health == 0:
                    self.kill()
    # def shoot(self):
    #     self.cd.event_time = floor(pg.time.get_ticks() / 1000)
    #     if self.cd.delta > 0.1:
    #         print(pg.mouse.get_pos())
    #         print(self.pos)
    #         self.mouse_pos = pg.mouse.get_pos()
    #         p=Projectile(self.game, self.rect.x, self.rect.y)
    #         self.mouse_pos = pg.mouse.get_pos()
    #         if self.mouse_pos[0] < self.pos.x:
    #             p.speed *= -1
    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        #if the x value is greater or less than either side of the screen
        if self.rect.x > WIDTH or self.rect.x < 0:
            #then reverse the speed by doing *= -1 and move the Mob down by 32
            self.speed *= -1
        #checks for if the y value of the Mob is greater than the height of the screen
        if self.rect.y > HEIGHT:
            #if it is then set the y-value to 0
            self.rect.y = 0            
        self.collide_with_projectile(self.game.all_projectiles, self.health, True)
# The Wall Class is part of the group all_walls in which interacts with the Player
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
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.game=game
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 25
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()
        
# This is the Speed Class that is part of the class all_powerups which has a shared interaction between it and the Player
class Speed(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.speed_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.game=game
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass
# This is the Jump Class that is part of the class all_powerups which has a shared interaction between it and the Player
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
# this is the Coin Class
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
class Moving_wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((5*TILESIZE, TILESIZE))
        self.game=game
        self.image.fill(Blue)
        self.rect = self.image.get_rect()
        self.game=game
        self.rect.x = x
        self.rect.y = y
        # Each Block is the size of 32 by 32 pixels or 1 TILESIZE ( in settings)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 5
        #create if statement to make the Platforms bounce back when they hit the wall
    # this method updates the Mob sprite so that it is always checking whether it is touching the side of the
    # screen, so it can go backwards using an if statement.
    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        #if the x value is greater or less than either side of the screen
        if self.rect.x > WIDTH - TILESIZE or self.rect.x < 0:
            self.speed *= -1