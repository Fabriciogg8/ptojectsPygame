# Nuestras clases de sprite para el juego de plataforma
import pygame as pg
from settings import *
# creamos una variable llamar al metodo de pygame que nos deja utilizar vectores
vec = pg.math.Vector2

class Player (pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game # este argumento es para que el jugador conozca todo lo que pasa en el juego por lo que podemos hacer que sepa que hay plataformas y entonces que responda a estas para por ej. saltar
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40,60))
        self.image.fill(P_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        # solo salta si está arriba de una plataforma
        hits = pg.sprite.spritecollide(self, self.game.platforms, False) # colisionamos nosotros mismos (Player) con la plataforma
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        # nuestra flecha controla la aceleracion del vector
        self.acc = vec(0,PLAYER_GRAV) 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        # movimiento de acuerdo a la fisica del mundo real
        # aplicamos friccion
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # ecuaciones de movimiento
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc # la posicion se le suma la velocidad mas la mitad de las aceleracion
        # no lo dejamos ir afuera de la pantall
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__ (self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(PL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



