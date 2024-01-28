import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# CREAMOS LA CLASE PARA NUESTRO PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(100,300))

    def update(self):
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
    screen.fill(GREEN)
    all_sprites.draw(screen)
    # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
    pygame.display.flip()

pygame.quit()