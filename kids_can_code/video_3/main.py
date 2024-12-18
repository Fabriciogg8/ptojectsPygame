import sys
import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

#Colocamos aca la funcion pero despues deberiamos sacarla
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0 
    BAR_LENGHT = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGHT
    outline_rect = pg.Rect(x,y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300, 100) #esto se utiliza para las teclas, para que cuando se mantiene apretada la flecha se mueva ARGS 1- Cuanto espera para empezar a repetir (originalmente 500, yo le puse 300), 2- Cada cuantos segundos repite, si el numero es muy grande demora mas en moverse
        self.load_data()
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        map_folder = path.join(game_folder, "maps")
        self.map = TiledMap(path.join(map_folder, "map1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (35, 35))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (35, 35))
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (55, 55))

    def new(self):
        # inicializa todas las variables y hace el todo el setup para un nuevo juego
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        # leemos el txt para crear el mapa
        # for row, tiles in enumerate(self.map.data):  # row 0 es igual a y=0 (ya que representa la horizontal), tiles es una fila con todos los puntos o 1
        #     for col, tile in enumerate(tiles): # col 0  es igual a x=0 (respresenta la vertical)
        #         if tile == "1":
        #             Wall(self,col, row) 
        #         if tile == "P":
        #             self.player = Player(self, col,row)
        #         if tile == "M":
        #             self.mob = Mob(self, col,row)
        for tile_object in self.map.tmxdata.objects: #para cada objeto en nuestra object layer del mapa vamos a obtener un diccionario, donde las propiedades son las llaves con sus respectivos valores
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "hitman":
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

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
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
    
    def events(self):
        # Game loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug #si es verdadera la cambia a false y si es False la cambia a True
                
    def draw_grid(self):
        #dinujamos la grilla x lineas horizontales e y lineas verticales
        for x in range (0, WIDTH, TILESIZE): # acordarse el utlimo argumento del rango es el salto que le vamos a dar, en este caso de a 32 que es el TILESIZE
            pg.draw.line(self.screen, WHITE,(x,0),(x,HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE,(0,y),(WIDTH,y))

    def draw(self):
        # Game loop - Draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1) #el ultimo argumento es el tamano del rectangulo
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)


        draw_player_health(self.screen, 20, 20, self.player.health/ PLAYER_HEALTH)
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