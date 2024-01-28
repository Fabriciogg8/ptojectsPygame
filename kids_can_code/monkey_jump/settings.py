# GAME OPTIONS / SETTINGS
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Earthelp"
FONT_NAME = "arial"

# Propiedades del player
PLAYER_ACC = 0.5 # aceleracion
PLAYER_FRICTION = -0.12 # friccion
PLAYER_GRAV = 0.6 # gravedad
PLAYER_JUMP = 20 # salto

# Plataformas iniciales
PLATFORM_LIST = [(0,HEIGHT - 40, WIDTH, 40),
                (WIDTH / 2 + 40, HEIGHT * 0.75, 100, 20),
                (WIDTH / 2 - 10, HEIGHT * 0.5, 100, 20),
                (350, HEIGHT -450, 100, 20),
                (15, 200, 100, 20)]


# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P_COLOR = (171, 235, 52)
PL_COLOR = (78, 194, 112)