#This file was created by: Umar Khan
player_speed=3
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
        self.mouse_pos = (0,0)
        self.health = 5
        self.invulnerable = Cooldown()
        self.jump_clock = Cooldown()
        self.mobs_can_attack= True
        self.cd = Cooldown()
        self.jump_power = 15
        self.jumping = False
        self.speed = player_speed
    #uses the typing library to collect input data from keyboard and make decisions based on it
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
        # if pg.mouse.get_pressed()[0]:
        #     self.shoot()
        if keys[pg.K_q]:
            self.shoot()
        if keys[pg.K_r]:
            self.game.new()
        self.mouse_pos = pg.mouse.get_pos()
        '''
        If the level is the startmenu and the level selected button hasn't been clicked yet than if the mouse_pos is in the range of the button
        and the mouse is pressed: Then click the levels button which set the level selected variable to true. In game if it is true than the levels appear as text.
        If their range is pressed than switch to those levels using self.game.level_chosen and self.game.level trough self.game.next_stage.
        '''
        if self.game.level == 'startmenu.txt' and self.game.levels_button_clicked == False:
            if self.mouse_pos[0] < 578 and self.mouse_pos[0] > 451 and self.mouse_pos[1] < 372 and self.mouse_pos[1] > 322 and pg.mouse.get_pressed()[0]:
                self.game.levels_button_clicked = True
            # if self.game.level == 'startmenu.txt' and self.game.levels_button_clicked == True:
            #     if self.mouse_pos[0] < 578 and self.mouse_pos[0] > 451 and self.mouse_pos[1] < 372 and self.mouse_pos[1] > 322 and pg.mouse.get_pressed()[0]:
            #         self.game.levels_button_clicked = False
        if self.game.level == 'startmenu.txt' and self.game.levels_button_clicked == True:
                if self.mouse_pos[0] > 460 and self.mouse_pos[1] < 560:
                    if self.mouse_pos[1] < 416 and self.mouse_pos[1] > 384 and pg.mouse.get_pressed()[0]:
                        print("1 plz")
                        self.game.level = self.game.chosen_level = 'lvl1.txt'
                        self.game.level_chosen = True
                    if self.mouse_pos[1] < 480 and self.mouse_pos[1] > 448 and pg.mouse.get_pressed()[0]:
                        print("2 plz")
                        self.game.level = self.game.chosen_level = 'lvl3.txt'
                        self.game.level_chosen = True
                    if self.mouse_pos[1] < 544 and self.mouse_pos[1] > 512 and pg.mouse.get_pressed()[0]:
                        print("3 plz")
                        self.game.level = self.game.chosen_level = 'lvl4.txt'
                        self.game.level_chosen = True
                    self.game.next_stage(self.game.chosen_level)

    # The projectile sprite is created and shot at speeds. The directions are determined by mouse_pos and to shoot is derived from mouse_get_pressed in get_keys.
    def shoot(self):
        self.cd.event_time = floor(pg.time.get_ticks() / 1000)
        if self.cd.delta > 0.01:
            self.mouse_pos = pg.mouse.get_pos()
            p=Projectile(self.game, self.rect.x, self.rect.y)
            print(self.mouse_pos)
            print(self.pos.y)
            if self.mouse_pos[1] > self.pos.y:
                p.speed *= -1
    def jump(self):
        self.rect.y += 2
        whits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        phits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if whits or phits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
        
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
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    # collide_with_stuff creates interactions between the all_powerups groups and can change the speed, jump_power,
    # This is also used for collision with other moving entities like Mobs and Bosses in which affects their health and the Player's health
    def collide_with_stuff(self,group,kill):
        hits=pg.sprite.spritecollide(self,group,kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Speed":
                print("I got one")
                self.speed+=5
            if str(hits[0].__class__.__name__) == "Coin":
                print("You got a Coin!")
                self.coins +=1
                self.game.total_coins += 100
            if str(hits[0].__class__.__name__) == "Jump":
                print("Jump Boost!")
                self.jump_power+=2
            if str(hits[0].__class__.__name__) == "Heart":
                self.health += 1
            if str(hits[0].__class__.__name__) == "Mob":
                self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                # hits[0].image = self.game.mob_img
                if self.invulnerable.delta > .01:
                    self.health -= 1
                if self.vel.y > 0:
                    print("collided with mob")
                else:
                    print("ouch I was hurt!!!")
            if str(hits[0].__class__.__name__) == 'Boss':
                self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                if self.invulnerable.delta > .01:
                    self.health -= 1
                if self.vel.y > 0:
                    print("collided with mob")
                else:
                    print("ouch I was hurt!!!")
            if str(hits[0].__class__.__name__) == "Trampoline":
                self.jump_clock.event_time = floor(pg.time.get_ticks()/1000)
                self.jump_power += 5
                if self.jump_clock.delta > 1:
                    self.jump_power -= 5

            if str(hits[0].__class__.__name__) == "Portal" and self.game.collisions_with_portal == 0 and self.game.bonus_achieved == False:
                self.game.collisions_with_portal = 1
                self.game.next_stage('bonus.txt')
                self.game.bonus_achieved = True
            if self.coins == self.game.coins_per_level and self.game.bonus_achieved == True:
                self.game.collisions_with_portal = 2
            if str(hits[0].__class__.__name__) == "Portal" and self.game.collisions_with_portal == 2 and self.game.bonus_achieved == True and self.coins == self.game.coins_per_level:
                self.game.next_stage(self.game.level)  
                self.game.bonus_achieved = 0
            if str(hits[0].__class__.__name__) == "Boss_Bullet":
                self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                # hits[0].image = self.game.mob_img
                if self.invulnerable.delta > .01:
                    self.health -= 1
                if self.vel.y > 0:
                    print("collided with mob")
                else:
                    print("ouch I was hurt!!!")

# The game always runs this code. Inside it goes if statements to determine changing parts of the game like collisions, score, and other stats/values.
    def update(self):
        self.cd.ticking()
        self.invulnerable.ticking()
        self.jump_clock.ticking()
        if self.health == 0:
            self.game.next_stage(self.game.level)
            self.health = 5
        self.pos += self.vel + 0.5 * self.acc
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_portals, False)
        self.collide_with_stuff(self.game.all_projectiles, False)
        self.collide_with_stuff(self.game.all_bullets, False)
        # self.collide_with_boss_bullet(self.game.all_projectiles)
# added Mob - moving objects
#is a child class of Sprite
# The Mob is in the group of all_mobs in which above the interactions between Mobs and Players can be created
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.mob_skin = self.game.mob_img
        # self.image = pg.Surface((32, 32))
        # self.image = self.mob_skin
        self.image = self.game.mob_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        # self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 3
        # Each Mob is the size of 32 by 32 pixels or 1 TILESIZE ( in settings)
        #the speed of the Mob is set to 30
        self.speed = random.randint(10,35)
        #create if statement to make the Mobs bounce back when they hit the wall
    # this method updates the Mob sprite so that it is always checking whether it is touching the side of the
    # screen, so it can go backwards using an if statement.

    # This determines the Mob's interaction with the Projectile shot by the Player.
    def collide_with_projectile(self,group,kill, health):
            hits=pg.sprite.spritecollide(self,group,kill)
            if hits:
                if str(hits[0].__class__.__name__) == "Projectile":
                    self.health -= 1
                    print("oof")
                if self.health == 0:
                    print("wasted")
                    self.kill()
    def update(self):
        self.image = self.game.mob_img
        self.image.set_colorkey(Black)
        # print(self.health)
        # if self.health < 3:
        #     self.mob_skin = self.game.mob_3_img
        #     print("hi")
        # if self.health < 3:
        #     self.game.mob_image = 'mob_full_health.png'
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

# The Player stands on these solid Tilesizes which are Walls. They make up the blocks of the game.
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wall_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    def update(self):
        pass
# This is the bullet the Player shoots to damage mobs and bosses
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bullet_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 25
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
# This is the Level 3 Boss's rockets in which he kills/damages the Player with. It is a spin-off of the Projectile from the Player.
class Boss_Bullet(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_bullets
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.boss_bullet_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 20
        # self.image = self.game.boss_Bullet_img
    def update(self):
        if self.game.end_game == False:
            self.rect.y += self.speed
        if self.game.end_game == True:
            self.image = self.game.nuke_img
            self.rect.x -= self.speed
        if self.rect.y > HEIGHT:
            self.kill()
        
        # self.rect.x = self.Boss.boss_xpos.x + move
        
# This is the Speed Class that is part of the class all_powerups which has a shared interaction between it and the Player
class Speed(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.speed_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass

# This powerup allows the player to collide with it in collide_with stuff to enter the bonus levels(in main.py).
class Portal(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_portals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.portal_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        if self.game.collisions_with_portal == 2 and self.game.bonus_achieved == 0:
            self.kill()
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
# if this sprite collides with the player it gives it additional health providing an alternative goal in the game besides coins and new levels.
class Heart(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.heart_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass
# this is the Coin Class. Players must collect this to gain score and points and to pass to the next level.
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.coin_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
    def update(self):
        pass
# This is a spin-off of the Wall with a speed element from Mob. It is created to increase mobility and challenge in the game as it provides a different type of wall.
class Moving_wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((5*TILESIZE, TILESIZE))
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.moving_wall_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Each Block is the size of 32 by 32 pixels or 1 TILESIZE ( in settings)
        self.x = x * 5*TILESIZE
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
class Trampoline(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.trampoline_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
    def update(self):
        pass
'''
This is level 3's boss. It is a spin-off of the Mob class in which it moves like it and has the same image/skin, but bigger. It shoots bullets which are like 
projectiles that the Player shoots, but they damage the Player's health. The boss has a second faze after it reachers 3 out of 5 hp where it spams horizontal missiles instead of its randomized vertical ones.
I used random.randint to check in update if the Mob reaches a random x point in which it will stop and fire missiles for 3 seconds before resuming it's horizontal movement.
The utilities timer was used.
'''
class Boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites , game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((5*TILESIZE, TILESIZE))
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.boss_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 5
        # Each Block is the size of 32 by 32 pixels or 1 TILESIZE ( in settings)
        self.x = x * 5*TILESIZE
        self.y = y * TILESIZE
        self.boss_xpos = self.rect.x
        self.speed = 30
        self.cooldown=Cooldown()
        self.rapid_cooldown=Cooldown()
        self.game.end_game = False
        self.rando=0
        # self.bullet_speed = 20
        # self.drop_speed=30
        #create if statement to make the Platforms bounce back when they hit the wall
    # this method updates the Mob sprite so that it is always checking whether it is touching the side of the
    # screen, so it can go backwards using an if statement.
    def boss_shoot(self):
        # self.player.cd.event_time = floor(pg.time.get_ticks() / 1000)
        # if self.player.cd.delta > 0.01:
            if self.game.end_game == False:
                self.move = random.randint(-50,50)
                b=Boss_Bullet(self.game, self.rect.x, self.rect.y)
            if self.game.end_game == True:
                t=Boss_Bullet(self.game, 1050, self.rando)
    def collide_with_thing(self,group,kill, health):
            hits=pg.sprite.spritecollide(self,group,kill)
            if hits:
                if str(hits[0].__class__.__name__) == "Projectile":
                    self.health -= 1
                    print("oof")
    def update(self):
        self.rando = random.randint(550,650)
        self.collide_with_thing(self.game.all_projectiles, self.health, True)
        self.cooldown.ticking()
        self.rapid_cooldown.ticking()
        self.rect.x += self.speed
        self.rn_time=self.cooldown.ticking()
        # self.rect.y += self.speed
        #if the x value is greater or less than either side of the screen
        if self.rect.x > WIDTH - TILESIZE or self.rect.x < 0:
            self.speed *= -1
        if self.health > 3:
            r= random.randint(0,30)
            if self.rect.x == r*30:
                self.speed = 0
                if self.speed == 0:
                    self.cooldown.event_time = floor(pg.time.get_ticks()/1000)
                    self.boss_shoot()
                    if self.cooldown.delta >= 2:
                        self.speed = 30
        if self.health <= 3 and self.health > 0:
            print("lock in")
            self.game.end_game = True
            self.rect.x = WIDTH // 2
            self.rect.y = HEIGHT//3
            self.rapid_cooldown.event_time = floor(pg.time.get_ticks()/1000)
            if self.rapid_cooldown.delta > 0.4:
                self.boss_shoot()
            if self.health < 1:
                print("mission success")
                self.game.boss_beaten = True
                if self.game.boss_beaten == True:
                        self.kill()