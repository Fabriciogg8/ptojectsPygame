import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# CREAMOS LA CLASE PARA NUESTRO PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p2_jump.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100,300))
        self.y_speed = 3


    def update(self):
        # self.rect.x += 4
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -3
        if self.rect.top < 200:
            self.y_speed = 5
            self.rect.x += 4
        if self.rect.left > WIDTH:
            self.rect.x = 0

# inicia pygame y crea la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earthelp")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    # Mantener el programa corriendo a la velocidad adecuada
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    all_sprites.update()

    # Draw/Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
    pygame.display.flip()

pygame.quit()