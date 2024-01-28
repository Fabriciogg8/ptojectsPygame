#Juego plataforma
import pygame as pg
import random
from settings import *
from sprites import *

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

    def new(self):
        # Empieza un juego nuevo
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self) # el self entre parentesis es para que el jugador conozca todo lo que pasa en el juego por lo que podemos hacer que sepa que hay plataformas y entonces que responda a estas para por ej. saltar
        self.all_sprites.add(self.player)
        # agregamos una plataforma
        for plat in PLATFORM_LIST:   
            p = Platform(*plat) # como tenemos los argumentos en una tupla tenemos que hacer este proceso para que p tenga cada uno de los valores, sino no puede iterar
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        # Game loop - Update
        self.all_sprites.update()
        # chequea si el jugador toca una plataforma, solo si esta cayendo
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # Scrol a la ventana si el player llega al 1/4 superior de la ventana
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y) # abs por el valor absoluto, ya que el movimiento hacia arriba resta a las y
            for plat in self.platforms: # hacemos lo mismo para las plataformas
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10 # le damos puntaje cuando sacamos las plataformas de la pantalla
        # hacemos mas plataformas para mantener la cantidad promedio en el juego
        while len(self.platforms) < 6:
            width = random.randrange(50,100)   
            # p ARGS- 1-x 2-y 3-largo y 4-ancho
            p = Platform(random.randrange(0,WIDTH - width),
                        random.randrange(-75, -30),
                        width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)
        # Muere el player!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10) #seleccionamos un maximo entre la velocidad de caida y 10
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False

        
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

    def draw(self):
        # Game loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Score: {self.score}", 22, WHITE, WIDTH/2, 15)
        # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
        pg.display.flip()

    def show_start_screen(self):
        # Game splash / start screen
        pass

    def show_go_screen(self):
        # Game over / continue
        pass

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