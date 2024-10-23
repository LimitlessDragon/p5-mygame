# this file was created by: Umar Khan
import random
#this is where we import libaries and modules
import pygame as pg
from settings import *
from spritescoin import *
#from sprites import *
from tilemap import *
from os import path
from utilities import *
'''
Goals:
To finish all the different levels by collecting all the coins in each level without getting hit my mobs.
Powerups will be provided differently in each level to make the game harder or easier.
Rules: You can't touch mobs; you can't reuse powerups;
Feedback: Colliding with mobs bounces them back, while colliding with coins earns you a point and gets you to the next level.
Powerups will disappear when collided with and give different effects depending on the type
Freedom: Sideways Movement; Powerups;Debufs; vertical movement with regard to gravity

Player 1 collides with powerup which gives it a speed boost.

'''
# create a game class that carries all the properties of the game and methods
class Game:
  def __init__(self):
    pg.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chris' Coolest Game Ever...")
    self.playing = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'lvl1.txt'))
  def load_level(self, level):
    self.map = Map(path.join(self.game_folder, level))
    # create game countdown timer
    self.game_timer = Timer(self)
    # # set countdown amount
    self.game_timer.cd = 60
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
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
          Jump(self,col*TILESIZE, row*TILESIZE)
        if tile == 'C':
          #draws a Coin where C is there
          Coin(self,col*TILESIZE, row*TILESIZE)
  # def game_over(self):
  #   print("Its Over!!!!!!!")
  #   self.load_level("lvl2.txt")
  def new(self):
    self.load_data()
    #create game countdown
    self.game_timer= Timer(self)
    #countdown time
    self.game_timer.cd = 50
    # create sprite group using the pg library
    self.all_sprites = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    # self.mob = Mob(self, 0, 0)
    # self.wall = Wall(self, WIDTH//2,HEIGHT//2)
    # #added sprites(player, mob, etc...) to the all_sprites group already in sprites in sprites
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
          Jump(self,col*TILESIZE, row*TILESIZE)
        if tile == 'C':
          #draws a Coin where C is there
          Coin(self,col*TILESIZE, row*TILESIZE)
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
      # output
      self.draw()

    pg.quit()
  # if you close the screen, everything else stops running
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # Makes sure the sprites are constantly being update on the screen with their values/data
  def update(self):
    print(self.game_timer.cd)
    self.game_timer.ticking()
    if self.game_timer.cd < 40:
      for s in self.all_sprites:
        s.kill()
        self.load_level("lvl2.txt")
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
  # game_over mechanism
  def game_over(self, level):
    print("Its Game Over!!!!")
    for s in self.all_sprites:
      s.kill()
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
          self.player = Player(self,col, row)
        if tile == 'U':
          #draws a Powerup where U is there
          Speed(self,col*TILESIZE, row*TILESIZE)
        if tile == 'J':
          #draws a Powerup where U is there
          Jump(self,col*TILESIZE, row*TILESIZE)
        if tile == 'C':
          #draws a Coin where C is there
          Coin(self,col*TILESIZE, row*TILESIZE)


  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    # Any text
    # self.draw_text(self.screen, "asdfdafddjfjdfjjdsfasdf", 24, White, WIDTH / 2, HEIGHT / 2)
    # Displays FPS and Coins
    self.draw_text(self.screen, str(self.dt*1000), 18, White, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.player.coins), 18, White, WIDTH-10, HEIGHT/30)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate the game; 
  g = Game()
  g.new()
  g.run()