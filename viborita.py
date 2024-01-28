import turtle
import time
import random

POSPONER = 0.1
# VARIABLES PARA EL MARCADOR
score = 0
high_score = 0

# CONFIGURACIÓN DE LA VENTANA
window = turtle.Screen()
window.register_shape("images_music/mario1.gif")
window.register_shape("images_music/hongo.gif")
window.register_shape("images_music/moneda.gif")
window.title("Juego de la viborita")
window.bgcolor("white")
window.setup(width=600, height= 600)
window.tracer(0) # HACE LAS ANIMACIONES MAS PLACENTERAS A NUESTROS OJOS


# CREACIÓN DE MARIO
mario = turtle.Turtle()
mario.shape("images_music/mario1.gif")
mario.penup()
mario.goto(0,0)
mario.direction = "stop"

# COLA DE MARIO
cola = []

# CREACIÓN DEL HONGO
hongo = turtle.Turtle()
hongo.shape("images_music/hongo.gif")
hongo.penup()
hongo.goto(50,50)
hongo.direction = "stop"

# CRACION DEL TEXTO
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("#40701E")
marcador.penup()
marcador.hideturtle()
marcador.goto(0,260)
marcador.write(f"SCORE: {score}           HIGH SCORE: {high_score}   ", align="center", font=("Cambria",20,"normal"))

# FUNCIONES
def up():
    mario.direction = "up"
def down():
    mario.direction = "down"
def left():
    mario.direction = "left"
def right():
    mario.direction = "right" 


def mov():
    if mario.direction == "up":
        mario.shape("images_music/hongo.gif")
        y = mario.ycor()
        mario.sety(y + 20)

    if mario.direction == "down":
        y = mario.ycor()
        mario.sety(y - 20)

    if mario.direction == "right":
        x = mario.xcor()
        mario.setx(x + 20)

    if mario.direction == "left":
        x = mario.xcor()
        mario.setx(x - 20)

#TECLADO
window.listen()
window.onkeypress(up, "Up") 
window.onkeypress(down, "Down")
window.onkeypress(left, "Left")
window.onkeypress(right, "Right")  

while True:
    window.update()


    # CHOCANDO EL BORDE
    if mario.xcor() > 280 or mario.ycor() > 280 or mario.ycor() < -280 or mario.xcor() < -280:
        time.sleep(1)
        mario.goto(0,0)
        mario.direction = "stop"
       
        # MANDANDO LAS COLAS FUERA DE LA PANTALLA
        for colita in cola:
            colita.goto(1000,1000)
        # LIMPIAMOS LA LISTA DE COLAS        
        cola.clear()

        # RESETEAMOS EL MARCADOR
        score = 0
        marcador.clear()    
        marcador.write(f"SCORE: {score}           HIGH SCORE: {high_score}   ", 
                                align="center", font=("Cambria",20,"normal"))  


    # CHOCANDO CON EL CUERPO, LA DISTANCIA DEBE SER MENOS A LA QUE SEPARAN A LA COLA DE LA CABEZA (ACA LE LLAMO MARIO)
    for colita in cola:
        if colita.distance(mario) < 20:
            time.sleep(1)
            mario.goto(0,0)
            mario.direction = "stop"  

            # MANDANDO LAS COLAS FUERA DE LA PANTALLA
            for colita in cola:
                colita.goto(1000,1000)
            # LIMPIAMOS LA LISTA DE COLAS        
            cola.clear()

            # RESETEAMOS EL MARCADOR
            score = 0
            marcador.clear()    
            marcador.write(f"SCORE: {score}           HIGH SCORE: {high_score}   ", 
                                align="center", font=("Cambria",20,"normal"))
 
        
    # CADA VEZ QUE SE ACERCA A MENOS DE 30px EL HONGO SE MUEVE PARA OTRO LADO DE MANERA RANDOM
    if mario.distance(hongo) < 30:
        x = random.randint(-280, 280)
        y = random.randint(-280, 260)
        hongo.goto(x,y)

        # CADA VEZ QUE TOQUE UN HONGO SE CREA LA COLA
        nueva_cola = turtle.Turtle()
        nueva_cola.speed(0)
        nueva_cola.shape("images_music/moneda.gif")
        nueva_cola.penup()
        cola.append(nueva_cola) # SE AGREGA EL SEGMENTO DE COLA EN LA LISTA COLA

        # AUMENTAMOS EL MARCADOR
        score += 10
        if score > high_score:
            high_score = score

        marcador.clear()    
        marcador.write(f"SCORE: {score}           HIGH SCORE: {high_score}   ", 
                                align="center", font=("Cambria",20,"normal")) 
   

    # AGREGAMOS EL MOVIMIENTO DE LA COLA
    largo_cola = len(cola)
    # El primer -1 le resta al valor del largo de la cola el último elemento 
    # el cero es porque no incluye el 0 en el rango. 
    # El ultimo -1 es para que vaya restando en el ciclo (primero 5, despues 4, etc)
    for colita in range(largo_cola -1, 0, -1):
        x = cola[colita - 1].xcor() # Se pide las coordenadas de la colita anterior y se las pasamos a la cola que le sigue
        y = cola[colita - 1].ycor()
        cola[colita].goto(x,y) # Le pasamos a la colita esos valores de x e y para que se mueva para ahí


    if largo_cola > 0:
        x = mario.xcor() 
        y = mario.ycor()  
        cola[0].goto(x,y)

    
    mov ()
    time.sleep(POSPONER)