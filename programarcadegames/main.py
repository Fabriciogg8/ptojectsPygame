# Importa  la libraría de funciones llamada 'pygame'
import pygame, sys, math
# Inicializa el motor de juegos
pygame.init() 

# Definir algunos colores
NEGRO  = (  0,   0,   0)
BLANCO = (255, 255, 255)
VERDE  = (0,   255,   0)
ROJO   = (255,   0,   0) 
AZUL   = (0,     0, 255)
BEIGE = (234, 182, 118) 

# Abrir y establecer las dimensiones de una ventana
dimensiones = (700, 500)
pantalla = pygame.display.set_mode(dimensiones) 

# Establecer el título de la ventana
pygame.display.set_caption("Epic Odyssey: Tale of the Nomad") 

# Itera hasta que el usuario pincha sobre el botón de cierre.
hecho = False
 
# Se usa para gestionar cuan rápido se actualiza la pantalla
reloj = pygame.time.Clock()
 
# -------- Bucle Principal del Programa -----------
while not hecho:
# 1------ Todos los eventos de procesamineto deberían ir debajo de este comentario
    for evento in pygame.event.get(): # El usuario hizo algo
        if evento.type == pygame.QUIT: # Si el usuario pincha sobre cerrar
            print("El usuario solicitó salir.")
            hecho = True # Esto que indica que hemos acabado y sale de este bucle
            pygame.quit() # Cierre correcto de un programa Pygame
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            print("El usuario presionó una tecla.")
        elif evento.type == pygame.KEYUP:
            print("El usuario soltó una tecla.")
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print("El usuario presionó un botón del ratón")
# 1------ Todos los eventos de procesamineto deberían ir encima de este comentario
 
# 2------ Toda la lógica del juego debería ir debajo de este comentario
 
# 2------ Toda la lógica del juego debería ir encima de este comentario
 
# 3------ Todo el código de dibujo debería ir debajo de este comentario
        # Limpia la ventana y establece el color del fondo
        pantalla.fill(BLANCO)
        
        # Dibujamos varias lineas
        for i in range(5):    
            pygame.draw.rect(pantalla, VERDE, [i, i**2, 10+i, i**4], width=5) # Dibujamos un rectangulo
            pygame.draw.line(pantalla, ROJO, (10,i**2),(200,i), width=10) # Dibujamos una linea
            pygame.draw.line(pantalla, BEIGE, (i**i,500),(700,0), width=50) 
        
        # Dibujamos varias lineas    
        for i in range(200): 
            radianes_x = i / 20
            radianes_y = i / 6
            x = int( 75 * math.sin(radianes_x) +i) + 55
            y = int( 75 * math.cos(radianes_y) +i) + 200
            pygame.draw.line(pantalla, NEGRO, [x, y], [x + 5, y], 5)
        
        # Representa una elipse, usando un rectángulo como perímetro exterior
        pygame.draw.ellipse(pantalla, NEGRO, [20, 20, 250, 100], 2)
        
        # Representa una arco
        pygame.draw.arc(pantalla, ROJO, [100, 100, 250, 200], 3*math.pi/2, 2*math.pi, 2)
        
        # Selecciona la fuente. Fuente Default, tamaño 25 pt.
        fuente = pygame.font.Font(None, 25)
        
        # Reproduce el texto. "True" significa texto suavizado(anti-aliased).
        # El color es Negro. Recordemos que ya hemos definido anteriormente la variable NEGRO
        # como una lista de (0, 0, 0)
        # Observación: Esta línea crea una imagen de las letras,
        # Pero aún no la pone sobre la pantalla.
        texto = fuente.render("Guillermina y Papi", True, NEGRO)
        numero = str(8)
        texto2 = fuente.render("Número: ", numero, True, NEGRO)

        # Coloca la imagen del texto sobre la pantalla 
        pantalla.blit(texto, [250, 250])
        pantalla.blit(texto2, [280, 280])
        
        # Avanza y actualiza la pantalla con lo que hemos dibujado.
        pygame.display.flip()
# 3------ Todo el código de dibujo debería ir encima de este comentario
  
        # Aquí limitamos el bucle while a un máximo de 60 veces por segundo.
        #Lo dejamos aquí y usamos toda la CPU que podamos.    
        reloj.tick(60)