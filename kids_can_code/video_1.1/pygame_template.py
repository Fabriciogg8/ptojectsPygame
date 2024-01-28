import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# inicia pygame y crea la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earthelp")
clock = pygame.time.Clock()

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
    # Draw/Render
    screen.fill(GREEN)
    # * Recordar que después de hacer todo el dibujo dar vuelta la pantalla * 
    pygame.display.flip()

pygame.quit()