import pygame 
from sys import exit
from random import randint

# INICIA PYGAME
pygame.init()
# PANTALLA LLEVA UNA TUPLA - ARGS 1-WIDTH (VALOR DE X) 2-HEIGHT (VALOR DE Y)
screen = pygame.display.set_mode((800, 400)) 
# TITULO JUEGO
pygame.display.set_caption("Earthelp")
# VELOCIDAD DEL JUEGO
clock = pygame.time.Clock()
# VARIABLE DE JUEGO ACTIVO
game_active = False
# VARIABLE QUE INICIALIZA EL SCORE EN 0
start_time = 0
# AHORA HACEMOS OTRA VARIABLE PARA EL SCORE
score = 0

# CREAMOS LA CLASE PARA NUESTRO HEROE
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("hero(3).png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100,300))

player = pygame.sprite.GroupSingle()
player.add(Player())

# CREAMOS UN TEXTO - ARGS 1-FONT TYPE 2-FONT SIZE
test_font = pygame.font.Font("Font/Pixeltype.ttf", 40)

# FUNCION PARA EL SCORE
def display_score():
    current_time = round((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'SCORE: {current_time}', False, "#40701E")
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    # PARA TENER LA VARIABLE current_time DE MANERA GLOBAL
    return current_time

# SUPERFICIES SE LES AGREGA .CONVERT PARA QUE PYGAME LAS MANEGE MEJOR
sky = pygame.image.load("bosque.png").convert()
pasto = pygame.image.load("pasto.png").convert()
# test_surface = pygame.Surface((100,200))
# test_surface.fill("Green") # COLOR DE LA SUPERFICIE

# CREAMOS LAS VARIABLES POSICIONALES DEL ENEMIGO
enemigo_1 = pygame.image.load("enemigo(1).png").convert_alpha()
enemigo_2 = pygame.image.load("enemigo(2).png").convert_alpha()
enemigo_3 = pygame.image.load("enemigo(3).png").convert_alpha()
enemy_frames_1 = [enemigo_1, enemigo_2, enemigo_3]
enemy_1_index = 0
enemy_1_surf = enemy_frames_1[enemy_1_index]
# enemigo_rect = enemigo.get_rect(midbottom=(600,300))
# NUEVO ENEMIGO
n_enemigo_1 = pygame.image.load("nuevo_enemigo.png").convert_alpha()
n_enemigo_2 = pygame.image.load("nuevo_enemigo(2).png").convert_alpha()
enemy_frames_2 = [n_enemigo_1, n_enemigo_2]
enemy_2_index = 0
enemy_2_surf = enemy_frames_2[enemy_2_index]
# n_enemigo_rect = n_enemigo.get_rect(midbottom=(600,300))
# CREAMOS UNA LISTA PARA AGREGAR LOS ENEMIGOS
obstacle_rect_list = []
# FUNCION PARA MOVER EL OBSTACULO
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for enemigo_rect in obstacle_list:
            enemigo_rect.x -= 2
            # SI EN EL RANDOM ELIGE UNO U OTRO CAMBIA LA POSICION DEL X, USAMOS ESO PARA IMPRIMIR EL ENEMIGO CORRECTO
            if enemigo_rect.bottom > 290:
                screen.blit(enemy_1_surf,enemigo_rect)
            else:
                screen.blit(enemy_2_surf,enemigo_rect)
        # HACEMOS UNA LIST COMPRHENSION PARA ELIMINAR LOS ENEMIGOS, COPIAMOS LOS ELEMENTOS A LA LISTA SOLO SI X ES MAYO A 0
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        # HACEMOS LA VARIABLE GLOBAL
        return obstacle_list
    # COMO ARRANCA VACIA DEVUELVE None Y SALTA ERROR AL HACER EL PRIMER APPEND, DEBMOS COLOCAR:
    else:
        return []

# FUNCION PARA LAS COLISIONES CON LOS ENEMIGOS
def collision (player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True        


# CREAMOS AL HEROE, ARMAMOS UNA LISTA PARA TODOS SUS CAMINATAS
hero_1 = pygame.image.load("hero(3).png").convert_alpha()
hero_2 = pygame.image.load("hero(2).png").convert_alpha()
hero_3 = pygame.image.load("hero(1).png").convert_alpha()
hero_walk = [hero_1, hero_2, hero_3]
hero_index = 0
hero_jump = pygame.image.load("hero(salta).png").convert_alpha()
hero_surf = hero_walk[hero_index]
# CREAMOS UN RECTANGULO PARA POSICIONAR BIEN AL HEROE, VAMOS A TENER VARIOS PUNTOS PARA POSICIONARLO, NO SOLO TOPLEFT QUE ES EL UNICO QUE PODES USAR SI NO UTILIZAS ESTE METODO
player_rect = hero_surf.get_rect(midbottom=(100,300))
player_gravity = 0

# CREAMOS LA FUNCIÓN PARA LA ANIMACION DEL HEROE
def hero_animation():
    global hero_index, hero_surf
    # VAMOS A DIFERENCIAR SI ESTA SALTANDO O CAMINANDO
    if player_rect.bottom < 300:
        hero_surf = hero_jump
    else:# VAMOS AGREGANDO POCO A POCO PARA LLEGAR DE 0 A 1
        hero_index += 0.1 
        # COMO SEGUIRA SUMANDO Y SE NOS IRÁ POR ENCIMA DEL LARGO DE NUESTRA LISTA (QUE EN MI CASO ES 2) DEBEMOS MANDARLO A CERO
        if hero_index >= len(hero_walk):
            hero_index = 0
        hero_surf = hero_walk[int(hero_index)]


# PARA LA PANTALLA DE INTRODUCCIÓN
hero_stand = pygame.image.load("hero(2).png").convert_alpha()
# PODEMOS PONERLO EN OTRA ESCALA ARGS: 1-MACACO 2-WIDTH 3-HEIGHT
# hero_stand = pygame.transform.scale(hero_stand,(200, 150))
# OTRA FORMA SCALE 2X
# hero_stand = pygame.transform.scale2x(hero_stand)
# OTRA FORMA ROTOZOOM ARGS: 1- SUPERFICIE(MACACO) 2-ANGULO 3-ESCALA
hero_stand = pygame.transform.rotozoom(hero_stand, 0, 2)
player_stand_rect = hero_stand.get_rect(midbottom=(400,300))
# CREAMOS LA SUPERFICIE PARA EL TEXTO - ARGS 1-TEXT 2-AA 3-COLOR
text_surface = test_font.render("EARTHELP", False, "#40701E")
text_rect = text_surface.get_rect(midbottom=(400,50))
game_message = test_font.render("Press space to jump", False, "#40701E")
game_message_rect = game_message.get_rect(midbottom=(400,360))

# CREAMOS UN TIMER PARA OBSTACULOS
obstacle_timer = pygame.USEREVENT + 1
# ARGS LA VARIABLE DEL EVENTO Y LOS MILISEGUNDOS QUE QUEREMOS QUE TRANSCURRAN ENTRE EVENTOS
pygame.time.set_timer(obstacle_timer, 1500)
# CREAMOS MAS TIMER PARA LAS ANIMACIONES DE LOS ENEMIGOS
enemy_1_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_1_timer, 100)
enemy_2_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_2_timer, 200)

# LOOP PARA CORRER EL PROGRAMA SIEMPRE
while True:
    # ANALIZAMOS TODOS LOS INPUT QUE PUEDE HACER EL USUARIO - 1 que cierre la ventana. 
    # DIBUJAMOS TODOS NUESTROS ELEMENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # ESTO ES LO OPUESTO A PYGAME.init()
            exit() # ESTE LO USAMOS PARA QUE PYTHON CIERRE BIEN EL WHILE LOOP

        if game_active:    
            #PODEMOS COLOCAR UN NUEVO IF PARA DISTINTAS SITUACIONES: MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ESTE LO UTILIZAMOS PARA SABER SI UN RECTANGULO CHOCA CON LA POSICION DEL MOUSE
                if player_rect.collidepoint(event.pos):
                    player_gravity -= 40
            # ESCUCHAMOS LAS TECLAS SI SE PRESIONAN O SE SUELTAN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                        player_gravity -= 40
            # if event.type == pygame.KEYUP:
            #     print("abajo")

            # EVENTO OBSTACULO
            if event.type == obstacle_timer:
                # TENEMOS UN IF QUE NOS MANDA 0 ó 1 Y AHI IMPRIME ó ENEMIGO 1 ó ENEMIGO 2 
                if randint(0,2):
                    obstacle_rect_list.append(enemy_1_surf.get_rect(bottomright=(randint(900,1800),300)))
                else:
                    obstacle_rect_list.append(enemy_2_surf.get_rect(bottomright=(randint(900,1800),290)))

            # HACEMOS EL CODIGO PARA EL CAMBIO DE DISFRAZ DE LOS ENEMIGOS SEGUN EL TIMER
            if event.type == enemy_1_timer:
                enemy_1_index += 1 
                # COMO SEGUIRA SUMANDO Y SE NOS IRÁ POR ENCIMA DEL LARGO DE NUESTRA LISTA (QUE EN MI CASO ES 2) DEBEMOS MANDARLO A CERO
                if enemy_1_index >= len(enemy_frames_1):
                    enemy_1_index = 0
                enemy_1_surf = enemy_frames_1[int(enemy_1_index)]
            if event.type == enemy_2_timer:
                if enemy_2_index == 0:
                    enemy_2_index = 1    
                else:
                    enemy_2_index = 0    
                enemy_2_surf = enemy_frames_2[enemy_2_index]


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # enemigo_rect.left = 800
                # LA VARIABLE VA AUMENTANDO A MEDIDA QUE EL JUEGO ESTA INICIADO, ENTONCES AL PERDER SE LE RESTA ESE TIEMPO A TIEMPO INICIAL PARA QUE VUELVA A CERO
                start_time = pygame.time.get_ticks()


    # CREAMOS EL IF DE LOS COMANDOS SI EL JUEGO ESTÁ ACTIVO                    
    if game_active:
        
        # COLOCAMOS LA SUPERFICIE QUE QUEREMOS EN EL LUGAR QUE QUEREMOS
        screen.blit(pasto,(0,250))
        screen.blit(sky,(0,0))
        # DIBUJAMOS UN RECTANGULO Y LE DAMOS FORMA
        # pygame.draw.rect(screen,"White", text_rect)
        # pygame.draw.rect(screen,"White", text_rect,7)
        # # PRUEBA DIBUJAR UNA LINEA RECTA
        # pygame.draw.line(screen,"Green",(0,0),(800,400),5)
        # # PODEMOS HACER UNA RECTA QUE SIEMPRE SIGA AL MOUSE
        # pygame.draw.line(screen,"Green",(0,0),pygame.mouse.get_pos(),5)
        # PROBAMOS DIBUJANDO UN CIRCULO -ARGS:1-LEFT px 2-TOP px 3-WIDTH px 4-HEIGHT px 
        # pygame.draw.ellipse(screen,"Green",pygame.Rect(50,200,200,200))
        # screen.blit(text_surface,text_rect)
        
        # ASIGNAMOS LA FUNCION A LA VARIABLE SCORE PARA PODER ACCEDER EN CUALQUIER MOMENTO
        score = display_score()


        # LE DECIMOS AL ENEMIGO QUE SE MUEVE A LA IZQUIERDA UN NUMERO DE PIXEL
        # enemigo_rect.x -= 2
        # # LE DECIMOS AL ENEMIGO QUE SI EL VALOR DE X ES MENOR A 0 SE VAYA A LA OTRA PUNTA
        # if enemigo_rect.right <= 0:
        #     enemigo_rect.left = 800 
        # screen.blit(enemigo,enemigo_rect)
        # MOVIENDO EL OBSTACULO, LLAMAMOS LA FUNCION Y SOOBRESCRIBIMOS LA VARIABLE
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
          
        # MOVIMIENTO DEL HEROE PODEMOS AGARRAR CUALQUIERA DE LOS PUNTOS DEL RECTANGULO
        # player_rect.left += 1
        # LE AGREGAMOS LA GRAVEDAD
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300 
        hero_animation()
        screen.blit(hero_surf,player_rect)
        player.draw(screen)

        # COLISIONES
        # if player_rect.colliderect(enemigo_rect):
        #     game_active = False
            # pygame.quit() # ESTO ES LO OPUESTO A PYGAME.init()
            # exit()
        # LLAMAMOS LA FUNCION PARA LAS COLLISIONES SI LA FUNCION DEVUELVE FALSE SE SALE DEL CICLO, YA QUE game_active DEBE SER True SIEMPRE   
        game_active = collision(player_rect, obstacle_rect_list)


        # ESCUCHAMOS LAS TECLAS PARA SABER SI ESTAN PRECIONADAS O NO
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("jump")
    
       
    else:
        screen.fill("#03360a")
        screen.blit(hero_stand, player_stand_rect)
        # PARA QUE CUANDO NOS TOQUE UN ENEMIGO NO SE QUEDEN PARADOS AL LADO NUESTRO SIN DEJARNOS REINICIAR BIEN
        obstacle_rect_list.clear()
        # SI PERDEMOS MANDAMOS EL HEROE AL INICIO DE LA PANTALLA
        player_rect.midbottom = (100,300)
        # RESTABLECEMOS LA GRAVEDAD
        player_gravity = 0

        # COLOCAMOS EL SCORE EN LA PANTALLA DE INICIO
        score_message = test_font.render(f'Your score: {score}', False, "#40701E")
        score_message_rect = score_message.get_rect(midbottom=(400,100)) 
        screen.blit(text_surface,text_rect)
        
        # AGREGAMOS UNA CONDICION PARA QUE NO SE DESPLIEGUE EL SCORE SI ES IGUAL A CERO
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    # ACTUALIZA TODo
    pygame.display.update() 
    # CONTROLA LA VELOCIDAD
    clock.tick(60)

def run():
    pass


if __name__ == "__main__":
    run()