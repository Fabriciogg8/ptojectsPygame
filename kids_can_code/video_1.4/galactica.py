# AUDIO COPYRIGHT https://musiccompositionhacks.blogspot.com/2020/07/how-to-improvise-music-in-real-time.html
# ART IMG FROM Kenny-nl
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000 #variable para este juego, define la cantidad de milesimas de segundos con mayor poder en el arma

# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (205,133,63)
YELLOW = (218,165,32)


# inicia pygame y crea la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactica")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m) # AGREGAMOS LOS MOBS AL ALL_SPRITES GROUP
    mobs.add(m)        # AGREGAMOS LOS MOBS AL MOBS GROUP

def draw_shield_bar(surf,x,y,porcentaje):
    if porcentaje < 0:
        porcentaje = 0
    BAR_LENGTH = 100 # tamano de la barra
    BAR_HEIGHT = 10
    fill = (porcentaje/100) * BAR_LENGTH # esta formula nos da la opcion de agrandar la barra y el porcentaje que le resta sera el mismo
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #el utltimo numero representa el ancho del rectangulo en px

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i # para separar las imagenes de los aviones
        img_rect.y = y
        surf.blit(img, img_rect)

# pantalla de game over
def show_gover_screen():
    screen.blit(game_over_img, game_over_rect)
    draw_text(screen,  "SPACE FLIGHT", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen,  "Flechas para moverse, espacio para disparar", 18, WIDTH/2, HEIGHT/2.5)
    draw_text(screen,  "Presiona una tecla para comenzar", 18, WIDTH/2, HEIGHT/2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80,60))
        self.rect = self.image.get_rect(midbottom=(240,580))
        # self.rect.centerx = 240
        # self.rect.bottom = HEIGHT - 10
        self.radius = 30 
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250 #agregamos una demora para los disparos para que sean continuos
        self.last_shoot = pygame.time.get_ticks() 
        self.lives = 3
        self.hidden = False #esta variable es para que cuando muera lo ocultamos y luego reaparecemos el sprite
        self.hidden_timer = pygame.time.get_ticks() 
        self.power = 1 # nivel inicial de poder que despues modificamos con el powerup
        self.power_time = pygame.time.get_ticks() 

    def update(self):
        # si se termina el tiempo para el powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # mostrarse si esta oculto
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1000 :
            self.hidden = False
            self.rect.midbottom = (240,580)
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -9
        if keystate[pygame.K_RIGHT]:
            self.speedx = 9    
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0    

    def powerup(self):
        self.power += 1 
        self.power_time = pygame.time.get_ticks() 

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1: 
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2: # se podria hacer otro si nos cae otro rayo y estuvieramos en self.power == 3 y asi sucesivamente si seguimos agarrando escudos tipo gun
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # esconde al jugador temporalmente
        self.hidden = True
        self.hidden_timer = pygame.time.get_ticks() 
        # la forma de esconderlo sera sacarlo de la pantalla, sino hay que elminarlo del grupo y luego volver a ponerlo y es mas complicado
        self.rect.center = (WIDTH/2, HEIGHT + 200)

# MOB es utilizado generico para enemigo
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-130, -100)
        # Se puede hace un circulo por encima del sprite para que choque segun eso pero no me funciona, igual chocan bien
        self.radius = int(self.rect.width * 0.7 / 2) 
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedy = random.randrange(1, 8)
        # PARA QUE TAMBIÉN SE MEUVAN EN DIAGONAL
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # CUANDO LLEGA ABAJO LO MANDAMOS PARA ARRIBA, PERO PARA QUE NO APAREZCA EN EL MISMO LUGAR LO HACEMOS RANDOM OTRA VEZ
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-110, -20)
            self.speedy = random.randrange(1, 8)

# AGREGAMOS LA CLASE PARA LAS BALAS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # matamos la bala si sale del cuadro
        if self.rect.bottom < 0:
            self.kill

# agregamos la clase para mejoras, tener mejor arma o mejorar los escudos durante el juego (POWERUP)
class Pow(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5 #aparece la imagen en pantalla y empieza a salir
    
    def update(self):
        self.rect.y += self.speedy
        # matamos el powerup si sale del cuadro
        if self.rect.top > HEIGHT:
            self.kill

# AGREGAMOS LA CLASE PARA LAS EXPLOSIONES:
class Explosion (pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 105 # velocidad a la que se ven las imagenes de las explosiones

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center    



# Cargamos todos los graficos (logre cambiar el tamano del background)
background = pygame.image.load(path.join(img_dir, "backg2.png")).convert_alpha()
ancho_deseado = 480
alto_deseado = 600
background = pygame.transform.scale(background, (ancho_deseado, alto_deseado))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "spaceShip_Fabricio.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (17, 15))
bullet_img = pygame.image.load(path.join(img_dir, "spaceMissiles_002.png")).convert_alpha()
game_over_img = pygame.image.load(path.join(img_dir, "game_over.png")).convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
game_over_rect = game_over_img.get_rect()
meteor_images = []
meteor_list = ["meteorGrey_med1.png","meteorGrey_big2.png","meteorGrey_small1.png","meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert_alpha())
# cargamos las explosiones, tendremos dos listas dentro del dicc una para cuando el fuego es mas grande y pega en los meteoros y otra para cuando es mas chico y pega en la nave, para que funcione bien fijarse como puse el nombre de las imagenes a usar en la explosion
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for i in range (5):
    filename = 'explosion_0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert_alpha()
    img_lg = pygame.transform.scale(img, (80,80))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (25,25))
    explosion_anim["sm"].append(img_sm)

# loop para las imagenes de la explosion del avion
for i in range (6):
    filename = "exp_0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha() 
    img_player = pygame.transform.scale(img, (200,200))
    explosion_anim["player"].append(img_player)

# cargamos las imagenes del powerup
powerup_images = {}
shield_img = pygame.image.load(path.join(img_dir, "shield.png")).convert_alpha()
shield_img = pygame.transform.scale(shield_img, (80, 65))
powerup_images["shield"] = shield_img
gun_img = pygame.image.load(path.join(img_dir, "strong.png")).convert_alpha()
gun_img = pygame.transform.scale(gun_img, (80, 65))
powerup_images["gun"] = gun_img


# Cargamos todos los sonidos
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot.wav"))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, "Pickup_shield.wav"))
power_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup.wav"))
expl_sound = []
expl_list = ["Explosion_2.wav", "explosion.wav"]
for snd in expl_list:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
# sonido para cuando muere el player
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, "explosion_ship.wav"))
# sonido de fondo se carga distinto
pygame.mixer.music.load(path.join(snd_dir, "dj_synth_wave.mp3"))
pygame.mixer.music.set_volume(0.4)


# inicilizamos la musica de fondo antes del loop
pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_gover_screen()
        game_over = False
        # GRUPOS PARA LOS PERSONAJES, SEPARAMOS EL PLAYER DE LOS MOBS
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        player = Player()
        # RECORDAR COLOCARLO ACA YA QUE ACA ES DONDE SE ACTUALIZA (UPDATED) Y SE DIBUJA (DRAW)
        all_sprites.add(player)

        # HACEMOS UN RANGO PARA LOS MOBS
        for i in range(8):
            newmob()
       
        score = 0
    #--------------------------------------------------------------------------------------------------
    # Mantener el programa corriendo a la velocidad adecuada
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:  # lo borramos porque lo agregamos en la clase player
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()

    #---------------------------------------------------------------------------------------------------
    # Update
    all_sprites.update()

    #vamos a compronar si una bala choca el mob (acordarse que son varias balas y varios mob por eso se usa groupcollide)
    #los True se usan para borrar los elementos del grupo que chocan 1-mobs 2-bullets
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    #como matavamos a todos y no reaparecen (porque son 8 mobs en el rango nomas) creamos uno cada vex que lo matamos
    for hit in hits:
        random.choice(expl_sound).play()
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95: # es para el powerup, random.random() elige un numero entre 0 y 1.En este caso cuanto mas cerca de 1 menos probabilidad de que aparezca
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # vamos a comprobar si el player choca un powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            shield_sound.play()
            player.shield += random.randrange(5,25)
            if player.shield > 100:
                player.shield = 100
        if hit.type == "gun": 
            player.powerup()   
            power_sound.play() 

    #vamos a comprobar si un mob chocó el jugador ARGS- 4-Se le puede agregar como cuarto argumento uno que
    #se refiere al choque por medio de radius, se agrega: pygame.sprite.collide_circle
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2 
        newmob()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_die_sound.play()
            exp_death = Explosion(player.rect.center, "player")
            all_sprites.add(exp_death)
            player.hide() # tenemos que elminiar a la nabe y hacer una espera antes de cerrar para ver la explosion al perder
            player.lives -= 1
            player.shield = 100

    #si el jugador murio y la imagen de la explosion se termino de reproducir. alive() es una funcion de pygame para saber si un sprite existe o no
    if player.lives == 0 and not exp_death.alive():
        game_over = True


    #----------------------------------------------------------------------------------------------------
    # Draw/Render
    # screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, (f"SCORE: {score}"), 18, WIDTH / 2, 20)
    # Funcion para el escudo ARGS- 1-surface 2-pos x 3-pos y 4-variable que la regula
    draw_shield_bar(screen, 5,5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
    pygame.display.flip()

pygame.quit()