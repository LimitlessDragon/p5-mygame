# this file was created by: Umar Khan
import random
#this is where we import libaries and modules
import pygame as pg
from settings import *
from mysprites import *
#from sprites import *
from tilemap import *
from os import path
from utilities import *
from typing import *
'''
Sources:

Arth Murarka, Kyle Suhendraw, and Shahmeer Khan for suggestion of the Main Menu

Stat/Health bar from Chris Cozort
Original Classes(Player,Game, and Functioning Movement) from Chris Cozort

https://www.pygame.org/docs/ref/mouse.html - used to see if mouse is clicked

Pieces of Missile image
https://www.vecteezy.com/png/36940512-ai-generated-missile-png-supersonic-missile-png-war-head-png-warhead-png-nuclear-missile-png-military-weapon-png-explosive-shell-png-missile-transparent-background

Trampoline Image
https://www.pixilart.com/art/trampoline-sprite-for-gam-c1144d241cff7e5

Brick Wall image
https://es.pinterest.com/pin/550776229426196197/

Code for putting Images: from Mr. Cozort
Scratch.mit.edu and google.com for sprite images/ inspirations for Sprites

https://www.tpsearchtool.com/images/superboy-2d-game-character-sprites-276-by-pasilan-graphicriver
Sprite Images


I got an idea for my mob from this link:
https://www.vecteezy.com/vector-art/14762634-cute-red-monster-vector

Coin Image from Mario (Nintendo)
Heart Image from Sans- Undertale
Bullet from pixelart.com
'''
'''
Goals:
To finish all the different levels by collecting all the coins in each level without getting hit my mobs.
Powerups will be provided differently in each level to make the game harder or easier.
Rules: You can't touch mobs; you can't reuse powerups;
Feedback: Colliding with mobs hurts you, while colliding with coins earns you a point and gets you to the next level.
Powerups will disappear when collided with and give different effects depending on the type
Freedom: Sideways Movement; Powerups;Debufs; vertical movement with regard to gravity

Player 1 collides with powerup which gives it a speed boost.


New ideas to add/do:
NEW LEVELS - (1/2 levels added)
Moving Platforms- Done
Portals
Timer for Powerup
create a reset button(r)-fix the load_data error when I tried to do it
create a def current_level(): to save the level after you die
'''
def draw_stat_bar(surf, x, y, w, h, pct, fill_color, outline_color):
    if pct < 0:
        pct = 0
    BAR_LENGTH = w
    BAR_HEIGHT = h
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, Black, outline_rect)
    pg.draw.rect(surf, fill_color, fill_rect)
    pg.draw.rect(surf, outline_color, outline_rect, 2)
# create a game class that carries all the properties of the game and methods
class Game:
  def __init__(self):
    pg.init()
    self.chosen_level = None
    self.level_chosen = False
    self.bonus_achieved = False
    self.levels_button_clicked = False
    self.collisions_with_portal = 0
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Umar's Coolest Game Ever...")
    self.playing = True
    self.coins_per_level = 18
    self.next_level = 'lvl1.txt'
    self.level = 'startmenu.txt'
    self.total_coins = 0
    self.score = 0
    self.boss_beaten = False
    self.end_game = False
  # the load_data is used to get data files(png and txt) for level info or sprite images
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'startmenu.txt'))
    self.img_folder = path.join(self.game_folder, 'img')
    self.player_img = pg.image.load(path.join(self.img_folder, 'peach1.png'))
    self.speed_img = pg.image.load(path.join(self.img_folder, 'image.png'))
    self.mob_image = 'mob.png'
    self.mob_img = pg.image.load(path.join(self.img_folder, 'mob.png'))
    self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png'))
    self.heart_img = pg.image.load(path.join(self.img_folder, 'heart.png'))
    self.bullet_img = pg.image.load(path.join(self.img_folder, 'upbullet.png'))
    self.portal_img = pg.image.load(path.join(self.img_folder, 'portal.png'))
    self.wall_img = pg.image.load(path.join(self.img_folder, 'wall.png'))
    self.moving_wall_img = pg.image.load(path.join(self.img_folder, 'moving (2).png'))
    self.trampoline_img = pg.image.load(path.join(self.img_folder, 'trampoline2.png'))
    self.boss_img = pg.image.load(path.join(self.img_folder, 'Boss.png'))
    self.boss_bullet_img = pg.image.load(path.join(self.img_folder, 'boss_bullet.png'))
    self.nuke_img = pg.image.load(path.join(self.img_folder, 'nuke.png'))
    '''
    self.mob_3_img = pg.image.load(path.join(self.img_folder, 'mob_full_health.png'))
    Player.get_keys(self)
    
  def reset_Player(self):
    if self.player.keys[pg.K_r]:
      Game.reset_Player(self)
    Game.new(self)
  
    '''
    '''
  To load each level:
  1: Select a txt map from data
  2: Restart the Timers and cooldowns
  '''
  def load_level(self, level):
    self.loading= True
    self.map = Map(path.join(self.game_folder, level))
    # create game countdown timer
    self.game_timer = Timer(self)
    # # set countdown amount
    self.game_timer.cd = 60

  # This occurs when you first start up the game: Basically it resets everything to starting stats and initializes the groups and sprites in their positions
  def new(self):
    self.end_game = False
    self.load_data()
    self.chosen_level = 'startmenu.txt'
    coins_per_level=0
    self.boss_beaten = False
    #create game countdown
    self.game_timer= Timer(self)
    #countdown time
    self.game_timer.cd = 50
    # create sprite group using the pg library
    # create the different sprites groups to allow for batch updates and draw methods
    # This allows the same interactions between the Player and some classes, while also easily allowing different interactions
    self.all_sprites = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_projectiles= pg.sprite.Group()
    self.all_bullets= pg.sprite.Group()
    self.all_portals= pg.sprite.Group()
    self.level = 'startmenu.txt'
    self.level_chosen = False
    self.bonus_achieved = False
    self.levels_button_clicked = False
    self.collisions_with_portal = 0
    # enumerates the .txt files, so it can be read as columns and rows
    # It scans the columns and rows for specfic letters such as M to place a Mob. Each letter is a different Tile of 32 pixels.
    #for loop to add more walls/sprites from the group all_sprites
    #we are going to read the text file into pixels
    for row, tiles in enumerate(self.map.data):
        for col, tile in enumerate(tiles):
          if tile == '1':
            #if 1 is in the text file, then draw a wall
            Wall(self, col*TILESIZE, row*TILESIZE)
          if tile == 'M':
            #draws a Mob where M is there
            Mob(self,col*TILESIZE, row*TILESIZE)
          if tile == 'P':
            #draws a Player where P is there
            self.player=Player(self,col, row)
          if tile == 'U':
            #draws a Powerup where U is there
            Speed(self,col*TILESIZE, row*TILESIZE)
          if tile == 'J':
            #draws a Powerup where U is there
            Trampoline(self,col*TILESIZE, row*TILESIZE)
          if tile == 'C':
            #draws a Coin where C is there
            Coin(self,col*TILESIZE, row*TILESIZE)
          if tile == 'A':
            #draws a moving wall
            Moving_wall(self, col*TILESIZE, row*TILESIZE)
          if tile == 'H':
            #draws a Powerup where U is there
            Heart(self,col*TILESIZE, row*TILESIZE)
          if tile == 'p':
            Portal(self,col*TILESIZE, row*TILESIZE)
          if tile == 'B':
            self.Boss=Boss(self,col*TILESIZE, row*TILESIZE)
    #drawing_sprites(self)

  '''
  Funny wall generator
    #for i in range(6):
      #w=Wall(self,i*HEIGHT//20,i*WIDTH//20)
    #Funny random Mob generator
    #for i in range(5):
      #m=Mob(self,TILESIZE*i,TILESIZE*2*i*random.random())
  '''
# this is a method
# methods are functions that are part of a class
# the run method runs the game loop in which is ticking to set the FPS
# After, it updates and draws the screen
  def run(self):
    while self.playing:
      #clock for updating the screen. Set the fps to 30.
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # outputa
      self.draw()

    pg.quit()
  # if you close the screen, everything else stops running
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # Makes sure the sprites are constantly being update on the screen with their values/data
  def update(self):
    self.next_level_first(self)
    self.game_timer.ticking()
    self.tracking = self.player.rect.x
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
  '''
  When the total # of Coins are reached then the level is switched to the next level
  The next thing to do with this is to change other values like speed and health(maybe)
  Also, later I can make this more streamline with more levels like lvl_4.txt and lvl_5.txt in which I could scan the current level
  for amount of coins to check if all were collected before switching.
  '''
  #Change the value for the if statement to a variable amount that changes for each level
  def next_level_first(self,level):
    if self.level != 'startmenu.txt' or self.level_chosen == True:
      if self.level == 'lvl1.txt':
        self.coins_per_level = 5
        self.next_level = 'lvl3.txt'
      if self.level == 'lvl3.txt':
        self.coins_per_level = 3
        self.next_level = 'lvl4.txt'
      if self.level == 'lvl4.txt':
        self.coins_per_level = 1
        self.next_level = 'loading.txt'
      if self.bonus_achieved == True:
        self.coins_per_level = 6
        self.next_level = self.level
      if self.level == 'loading.txt':
        self.coins_per_level == 994299242
      if self.player.coins == self.coins_per_level and self.bonus_achieved == False:
        if self.player.coins == self.coins_per_level and self.level != 'loading.txt':
          self.score += 500
          print("prepare")
        self.next_stage(self.next_level)
        print("next")
        self.level = self.next_level
      # if self.boss_beaten == True and self.level == 'lvl4.txt':
      #   self.score+=1000
      #   self.level = 'loading.txt'
      #   self.next_stage('loading.txt')
      #when player is recalled it resets the coins, so we put it back
      #change other stuff     
  '''
  next_stage mechanism: First kills all the mobs to clear memory.
  Then, it loads a new level which the argument used when it is
  called determines what stage is next which makes it useful
  in many cases such as: next level; game over; bonus level
  '''
  def next_stage(self, level):
    for s in self.all_sprites:
      s.kill()
      self.mob_image = 'mob.png'
    self.map = Map(path.join(self.game_folder, level))
    for row, tiles in enumerate(self.map.data):
        for col, tile in enumerate(tiles):
          if tile == '1':
            #if 1 is in the text file, then draw a wall
            Wall(self, col*TILESIZE, row*TILESIZE)
          if tile == 'M':
            #draws a Mob where M is there
            Mob(self,col*TILESIZE, row*TILESIZE)
          if tile == 'P':
            #draws a Player where P is there
            self.player=Player(self,col, row)
          if tile == 'U':
            #draws a Powerup where U is there
            Speed(self,col*TILESIZE, row*TILESIZE)
          if tile == 'J':
            #draws a Powerup where U is there
            Trampoline(self,col*TILESIZE, row*TILESIZE)
          if tile == 'C':
            #draws a Coin where C is there
            Coin(self,col*TILESIZE, row*TILESIZE)
          if tile == 'A':
            #draws a moving wall
            Moving_wall(self, col*TILESIZE, row*TILESIZE)
          if tile == 'H':
            #draws a Powerup where U is there
            Heart(self,col*TILESIZE, row*TILESIZE)
          if tile == 'p':
            Portal(self,col*TILESIZE, row*TILESIZE)
          if tile == 'B':
            self.Boss=Boss(self,col*TILESIZE, row*TILESIZE)

  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    if self.level == 'startmenu.txt':
      self.draw_text(self.screen, "Coin Collector", 64, Yellow, WIDTH // 2, HEIGHT - 18* TILESIZE)
      draw_stat_bar(self.screen, WIDTH - 18.5 * TILESIZE, HEIGHT - 14 * TILESIZE, 5*TILESIZE, 2*TILESIZE, 100, Yellow, Black)
      self.draw_text(self.screen, "Levels", 50, Black, WIDTH // 2, HEIGHT - 14* TILESIZE)
      # self.draw_text(self.screen, "Settings", 50, White, WIDTH // 2, HEIGHT - 14* TILESIZE)
    if self.levels_button_clicked == True and self.level == 'startmenu.txt':
      # draw_stat_bar(self.screen, WIDTH - 26 *TILESIZE, HEIGHT - 10 * TILESIZE, 15*TILESIZE, 2*TILESIZE, 100, Yellow, Black)
      # self.draw_text(self.screen, "Level 1", 24, Black, WIDTH - 24*TILESIZE, HEIGHT - 10* TILESIZE)
      # self.draw_text(self.screen, "Level 2", 24, Black, WIDTH - 20*TILESIZE, HEIGHT - 10* TILESIZE)
      # self.draw_text(self.screen, "Level 3", 24, Black, WIDTH - 16*TILESIZE, HEIGHT - 10* TILESIZE)
      draw_stat_bar(self.screen, WIDTH - 17.5*TILESIZE, HEIGHT - 8 * TILESIZE, 3*TILESIZE, 1*TILESIZE, 100, Yellow, Black)
      draw_stat_bar(self.screen, WIDTH - 17.5*TILESIZE, HEIGHT - 10 * TILESIZE, 3*TILESIZE, 1*TILESIZE, 100, Yellow, Black)
      draw_stat_bar(self.screen, WIDTH - 17.5*TILESIZE, HEIGHT - 12 * TILESIZE, 3*TILESIZE, 1*TILESIZE, 100, Yellow, Black)
      self.draw_text(self.screen, "Level 1", 24, Black, WIDTH //2, HEIGHT - 12* TILESIZE)
      self.draw_text(self.screen, "Level 2", 24, Black, WIDTH //2, HEIGHT - 10* TILESIZE)
      self.draw_text(self.screen, "Level 3", 24, Black, WIDTH //2, HEIGHT - 8* TILESIZE)
    # Any text
    # self.draw_text(self.screen, "asdfdafddjfjdfjjdsfasdf", 24, White, WIDTH / 2, HEIGHT / 2)
    # Displays FPS and Coins
    self.draw_text(self.screen, str(self.dt*1000), 18, White, WIDTH/30, HEIGHT/30)
    # Draw health bar
    # So, that if the end screen or home screen is there than it won't generate or leave the healthbar or the coins amount
    if self.level != 'loading.txt' and self.level != 'startmenu.txt':
      draw_stat_bar(self.screen, self.player.rect.x, self.player.rect.y-TILESIZE, TILESIZE, 25, 20*self.player.health, Green, White)
      self.draw_text(self.screen, ("Coins: "+str(self.player.coins)), 18, Yellow, self.player.rect.x - TILESIZE, self.player.rect.y - TILESIZE)
    if self.level == 'lvl4.txt':
      draw_stat_bar(self.screen, self.Boss.rect.x - TILESIZE, self.Boss.rect.y-TILESIZE, TILESIZE, 25, 20*self.Boss.health, Green, White) 
    '''
    This is where the end screen comes in. If the level is loading text than reload the level and display the end stuff: coins and game complete.
    I also put total_coins into Game as the player resets every level also resetting the coins.
    '''
    if self.level == 'loading.txt':
          # self.next_stage('loading.txt')
          self.draw_text(self.screen, "Game Complete!!!", 45, White, WIDTH // 2, HEIGHT // 2)
          self.draw_text(self.screen, "Coins: "+str(self.total_coins+self.score), 36, Yellow, WIDTH // 2, HEIGHT // 1.75)
    # draw_stat_bar(self.screen, self.mob.rect.x, self.mob.rect.y-TILESIZE, TILESIZE, 25, self.mob.health, Red, White)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate the game; 
  g = Game()
  g.new()
  g.run()