import sys
import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        
    def load_data(self):
        pass

    def new(self):
        # inicializa todas las variables y hace el todo el setup para un nuevo juego
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 0, 0)

    def run(self):
        # game loop - se setea self.playing = False para finalizar el juego
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()           
            self.events()
            self.draw()

    def update(self):
        # Game loop - Update
        self.all_sprites.update()
    
    def events(self):
        # Game loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()

    def draw_grid(self):
        #dinujamos la grilla x lineas horizontales e y lineas verticales
        for x in range (0, WIDTH, TILESIZE): # acordarse el utlimo argumento del rango es el salto que le vamos a dar, en este caso de a 32 que es el TILESIZE
            pg.draw.line(self.screen, WHITE,(x,0),(x,HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE,(0,y),(WIDTH,y))

    def draw(self):
        # Game loop - Draw
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()