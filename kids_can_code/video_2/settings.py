# GAME OPTIONS / SETTINGS
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Earthelp"
FONT_NAME = "arial"
HS_FILE = "High_score.txt"
SPRITESHEET = "mono.png"
BANANA = "bananas.png"
LORO = "loro.png"
RAMA = "rama.png"
RAMA2 = "rama_2.png"


# Propiedades del player
PLAYER_ACC = 0.5 # aceleracion
PLAYER_FRICTION = -0.15 # friccion
PLAYER_GRAV = 0.5 # gravedad
PLAYER_JUMP = 30 # salto

# Propiedades del juego
BOOST_POWER = 60
POW_SPAWN_PCT = 8  #frecuencia con la que parecen las bananas
MOBS_FREQ = 3000   #frecuencia con la que aparece un mob
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# Plataformas iniciales
PLATFORM_LIST = [(0,HEIGHT - 70), # Originalmente le dabamos altura y ancho, pero al utilizar las imagenes las cancelamos, porque las imagenes ya tienen un tamano
                (WIDTH // 2 - 50, HEIGHT * 3/4 - 50),
                (350, HEIGHT -350),
                (10, 200)]


# Definimos colores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P_COLOR = (171, 235, 52)
PL_COLOR = (78, 194, 112)
BACK_COLOR = (32, 66, 42)