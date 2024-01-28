# Nuestras clases de sprite para el juego de plataforma
import pygame as pg
from settings import *
import random
# creamos una variable llamar al metodo de pygame que nos deja utilizar vectores
vec = pg.math.Vector2

class Spritesheet:
    # Utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scalex, scaley):
        #agarra una imagen del spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0),(x, y, width, height))
        image = pg.transform.scale(image, (scalex, scaley))
        return image

class Player (pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game # este argumento es para que el jugador conozca todo lo que pasa en el juego por lo que podemos hacer que sepa que hay plataformas y entonces que responda a estas para por ej. saltar
        self.walking = False
        self.jumping = False
        self.standing = True
        self.current_frame = 0 
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(30, HEIGHT-330)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(0,0,50,39, 90, 80), 
                                self.game.spritesheet.get_image(44,00,50,39, 90, 80),
                                self.game.spritesheet.get_image(94,00,50,39, 90, 80),]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK) #le saca el color negro de fondo
       
        # en la imagen camina hacia la derecha, son estos r, pero para el left tenemos que darlos vuelta
        self.walk_frames_r = [self.game.spritesheet.get_image(150,00,50,39, 90, 80),
                            self.game.spritesheet.get_image(200,00,50,39, 90, 80),
                            self.game.spritesheet.get_image(250,00,50,39, 90, 80),
                            self.game.spritesheet.get_image(255,00,50,39, 90, 80),]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False)) # True giramos horizontalmente, False para que no lo haga verticalmente
            frame.set_colorkey(BLACK)
       
        self.jump_frames_r = [self.game.spritesheet.get_image(0,42,50,60, 100, 90), 
                                self.game.spritesheet.get_image(48,42,50,60, 100, 90),
                                self.game.spritesheet.get_image(100,42,50,60, 100, 90)]
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))
            frame.set_colorkey(BLACK)


    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -2: # si estamos yendo hacia arrbia mas rapido que 3 px
                self.vel.y = -2



    def jump(self):
        # solo salta si está arriba de una plataforma
        self.rect.y += 2 #aunque parece que no es necesario ponelos mejora el uso de la barra espaciadora para saltar, responde mejor
        hits = pg.sprite.spritecollide(self, self.game.platforms, False) # colisionamos nosotros mismos (Player) con la plataforma
        self.rect.y -= 2
        if hits and not self.jumping:
            random.choice(self.game.jump_sound).play() # cada vez que saltamos elige una opcion de los sonidos de salto
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
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
        if abs(self.vel.x) < 0.1: # esto se hace para que no quede mirando para el costado, sino que pare y muestre las imagenes de cuando esta parado, absoluto porque puede ser positivo o negativo el valor de x
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc # la posicion se le suma la velocidad mas la mitad de las aceleracion
        # para que al final de la pantalla aparezca del otro lado
        if self.pos.x > WIDTH + self.rect.width/ 2:
            self.pos.x = 0 - self.rect.width/ 2
        if self.pos.x < 0 - self.rect.width/ 2:
            self.pos.x = WIDTH + self.rect.width/ 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 and self.vel.y == 0:
            self.walking = True
            self.standing = False
            self.jumping = False
            if self.walking == True:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    bottom = self.rect.bottom
                    if self.vel.x > 0:
                        self.image = self.walk_frames_r[self.current_frame]
                    else:
                        self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        elif self.vel.y != 0:
            self.jumping = True
            self.walking = False
            self.standing = False
            if self.jumping == True:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                    bottom = self.rect.bottom
                    if self.vel.y < 0 and self.vel.x > 0:
                        self.image = self.jump_frames_r[self.current_frame]
                    elif self.vel.y < 0 and self.vel.x < 0:
                        self.image = self.jump_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        elif not self.jumping and not self.walking:
            self.standing = True
            self.walking = False
            self.jumping = False
            if self.standing == True:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)  #mascara para las colisiones mas exactas y no por el rectangulo


class Platform(pg.sprite.Sprite):
    def __init__ (self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet4.get_image (0,0,128,128, 128, 80),
                self.game.spritesheet5.get_image(0,0,128,128, 100, 80),]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # si el valor random elegido es menor a la fecuencia de aparicion de un powerups lo hacemos aparecer
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self) 

class Pow(pg.sprite.Sprite):
    def __init__ (self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups 
        pg.sprite.Sprite.__init__(self, self.groups) #para no tener que agregar contiuamente los sprites a los grupos es importante que se ponga antes de esta linea de codigo, lo anterior y agregamos en el init self.groups
        self.game = game
        self.plat = plat
        self.type = random.choice(["boost"])
        self.image = self.game.spritesheet2.get_image(0,0,808,589, 45, 35)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.rect.top - 10
    
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5 #para que cuando la plataforma se mueva igual este ahi la banana moviendose con ella
        if not self.game.platforms.has(self.plat): #has retorna True or False, si existe la plataforma o no en el grupo
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__ (self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups) #para no tener que agregar contiuamente los sprites a los grupos es importante que se ponga antes de esta linea de codigo, lo anterior y agregamos en el init self.groups
        self.game = game
        self.image_up = self.game.spritesheet3.get_image(5,20,50,50, 70, 70)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet3.get_image(395,20,50,50, 70, 70)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH+100])
        self.vx = random.randrange(1,4)
        if self.rect.centerx > WIDTH:
            self.vx = -1
        self.rect.y = random.randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5

   
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image) #mascara para las colisiones mas exactas y no por el rectangulo
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()