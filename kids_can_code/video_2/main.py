#Juego plataforma

# File I/O Input and output

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

class Game:
    def __init__(self):
        # Inicia la ventana del juego, etc.
        # inicia pygame y crea la ventana
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):    
        # Funcion donde se cargan todos las imagenes, audio, etc.
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'img')
        with open (path.join(self.dir, HS_FILE), "w") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # Cargamos las imagenes del spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet2 = Spritesheet(path.join(img_dir, BANANA))
        self.spritesheet3 = Spritesheet(path.join(img_dir, LORO))
        self.spritesheet4 = Spritesheet(path.join(img_dir, RAMA))
        self.spritesheet5 = Spritesheet(path.join(img_dir, RAMA2))
        self.background = pg.image.load(path.join(img_dir, "bc.png")).convert_alpha()
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()


        # Cargamos los sonidos
        self.snd_dir = path.join(self.dir, "snd")
        self.jump_sound = []
        self.jump_list = ["jump.wav", "jump2.wav"]
        for snd in self.jump_list:
            self.jump_sound.append(pg.mixer.Sound(path.join(self.snd_dir, snd)))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, "banana.wav"))


    def new(self):
        # Empieza un juego nuevo
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates() # te permite organizar como pones los sprites en la pantalla
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self) # el self entre parentesis es para que el jugador conozca todo lo que pasa en el juego por lo que podemos hacer que sepa que hay plataformas y entonces que responda a estas para por ej. saltar
        # agregamos una plataforma
        for plat in PLATFORM_LIST:   
            Platform(self, *plat) # como tenemos los argumentos en una tupla tenemos que hacer este proceso para que p tenga cada uno de los valores, sino no puede iterar
        self.mob_timer = 0  # hacemos una variable para cada vez que aparece un nuevo mob
        pg.mixer.music.load(path.join(self.snd_dir, "running.ogg")) #cargamos la musica del juego
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1) #le damos play a la musica del juego, el loops es para que no para de ejecutarse
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()
        pg.mixer.music.fadeout(500) # le decimos que cuando termina el run en medio segundo se va yendo para que no termine de golpe

    #--------------------------------------------------------------------------------------------------# 
    def update(self):
        # Game loop - Update
        self.all_sprites.update()

        # aparece un mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 3000 + random.choice([-1000,-500, 0, 500, 1000]):  # se pdria poner un rango pero no tiene sentido una diferencua de 1888 a 1889 por ejemplo, ya que son milisegundos, entonces se hace que elija entre una lista de valores de a medio segundo de diferencia
            self.mob_timer = now
            Mob(self)
       
        # choca con un mob
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask) # no importa en este caso True o False porque muere el player
        if mob_hits:
            self.playing = False

        # chequea si el jugador toca una plataforma, solo si esta cayendo
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom: # recordar que los valores de y van aumentando hacia abajo, entonces el que está mas abajo es el que tiene valor y mas grande
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 5 and self.player.pos.x > lowest.rect.left + 5 : # esto hace que no este el rectangulo arriba de la plataforma y los pies en el aire, sino que si el rectangulo llega al borde se cae, le agregamos unos pixeles para que quede mejor, pero si los sacas queda bien igual
                    if self.player.pos.y < lowest.rect.centery:  #con esta linea mejoramos que suba a una plataforma solo si los pies tocan un plataforma y no cualquier parte del cuerpo
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False # volvemos falsa la variable para que pueda volver a saltar si toca una plataforma
       
        # Scrol a la ventana si el player llega al 1/4 superior de la ventana
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2) # abs por el valor absoluto, ya que el movimiento hacia arriba resta a las y. Despues le agregamos el mx que elije el valor maximo, entre la velocidad del jugador o 2 en este caso, sino quedaba parada la pantalla cuando el player no se movia.
            for mob in self.mobs: # hacemos lo mismo para las mos
                mob.rect.y += max(abs(self.player.vel.y), 2)
                if mob.rect.top >= HEIGHT:
                    mob.kill()
            for plat in self.platforms: # hacemos lo mismo para las plataformas
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10 # le damos puntaje cuando sacamos las plataformas de la pantalla

        # hacemos mas plataformas para mantener la cantidad promedio en el juego
        while len(self.platforms) < 6:
            width = random.randrange(50,100)   
            # p ARGS- 1-x 2-y 3-largo y 4-ancho
            Platform(self, random.randrange(0,WIDTH - width),random.randrange(-100, -50))


        # si el jugador choca con la banana
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == "boost":
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
            

        # Muere el player!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10) #seleccionamos un maximo entre la velocidad de caida y 10
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False

    #--------------------------------------------------------------------------------------------------#  
    def events(self):
        # Game loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


    #--------------------------------------------------------------------------------------------------# 
    def draw(self):
        # Game loop - Draw
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        # self.screen.blit(self.player.image, self.player.rect) #para que el jugador no aparezca atras de las plataformas, lo dibujamos antes (LO SOLUCIONAMOS DESPUES CON LOS LAYER)
        self.draw_text(f"Score: {self.score}", 22, WHITE, WIDTH/2, 15)
        # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
        pg.display.flip()

    def show_start_screen(self):
        # Game splash / start screen
        #-------------------LO CARGUE YO--------------------------
        jungle_img = pg.image.load(path.join(img_dir, "jungle.png")).convert_alpha()
        jungle_img = pg.transform.scale(jungle_img, (500, 600))
        jungle_rect = jungle_img.get_rect()
        self.screen.blit(jungle_img, jungle_rect)
        #-----------------------------#
        pg.mixer.music.load(path.join(self.snd_dir, "intro.ogg"))
        pg.mixer.music.play(loops =-1)
        self.draw_text(TITLE, 56, BLACK, WIDTH/2, 50)
        self.draw_text("Flechas para moverse, espacio para saltar", 24, BLACK, WIDTH/2, 150)
        self.draw_text("Presiona una tecla para jugar", 24, WHITE, WIDTH/2, 500)
        self.draw_text(f"HIGH SCORE: {self.highscore}", 24, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # Game over / continue
        if not self.running: # esto es para poder cerrar el juego sin pasar por la pantalla game over, si estamos jugando y queremos cerrar todo, antes nos hacia ir primero a game over y despues en la cruz otra vez para cerrar
            return
        pg.mixer.music.load(path.join(self.snd_dir, "gover.ogg"))
        pg.mixer.music.play(loops =-1)
        go_img = pg.image.load(path.join(img_dir, "go_screen.png")).convert_alpha()
        go_img = pg.transform.scale(go_img, (671, HEIGHT))
        go_rect = go_img.get_rect()
        self.screen.blit(go_img, go_rect)
        self.draw_text("GAME OVER", 56, WHITE, WIDTH/2, 150)
        self.draw_text(F"FINAL SCORE: {self.score}", 24, WHITE, WIDTH/2, 250)
        self.draw_text("Presiona una tecla para continuar", 24, WHITE, WIDTH/2, 550)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("CONGRATULATIONS NEW HIGH SCORE!!", 24, WHITE, WIDTH/2, 350)
            with open(path.join(self.dir, HS_FILE),"w") as f:
                f.write(str(self.score))
        else:
            self.draw_text(f"HIGH SCORE: {self.highscore}", 24, WHITE, WIDTH/2, 350)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    # esta funcion se hace para esperar que presione una tecla para salir de la pantalla de inicio y empezar el juego    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


# g es una instancia de la clase Game()
g= Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen() #go es de game over

pg.quit()