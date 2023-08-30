import pygame
import sys
""" 
Funciones relevantes al funcionamiento interno del juego de reversi
"""
#generacion e inicialización de un tablero de 8x8 o 6x6
def generar_tablero_8():
    tablero=[]
    for i in range(8):
        tablero.append([0]*8)
    return tablero
def reiniciar_tablero_8(tablero):
    for x in range(8):
        for y in range(8):
            tablero[x][y]=0
    tablero[3][3]=1
    tablero[3][4]=2
    tablero[4][3]=2
    tablero[4][4]=1
def generar_tablero_6():
    tablero=[]
    for i in range(6):
        tablero.append([0]*6)
    return tablero
def reiniciar_tablero_6(tablero):
    for x in range(6):
        for y in range(6):
            tablero[x][y]=0
    tablero[2][2]=1
    tablero[2][3]=2
    tablero[3][2]=2
    tablero[3][3]=1
#validez de una jugada
def esta_en_tablero(tablero,x,y):
    return x>=0 and len(tablero[0])>x and y>=0 and len(tablero[0])>y
def movimiento_esvalido(tablero, pieza, xstart, ystart):
    #retorna falso si la jugada es invalida o está usada la posicion
    if tablero[xstart][ystart] != 0 or not esta_en_tablero(tablero,xstart,ystart):
        return False
    tablero[xstart][ystart] = pieza
    if pieza == 1:
        otrapieza=2
    else:
        otrapieza=1
    piezas_giradas=[]
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y= xstart,ystart
        x+=xdirection #primer paso en la direccion
        y+=ydirection
        if esta_en_tablero(tablero,x,y) and tablero[x][y] == otrapieza:
            #hay una pieza del jugador contrario a nuestra pieza
            x+=xdirection
            y+=ydirection
            if not esta_en_tablero(tablero,x,y):
                continue
            if tablero[x][y] == pieza:
                #hay piezas para voltear. reversa hasta el espacio original, anotando todas las piezas en el camino
                while True:
                    x-=xdirection
                    y-=ydirection
                    if x == xstart and y==ystart:
                        break
                    piezas_giradas.append([x,y])
    tablero[xstart][ystart]=0
    if len(piezas_giradas)==0:
        return False #si no se da vuelta ninguna figura, no es movimiento válido
    return piezas_giradas
def tablero_jugadas(tablero,pieza):
    #retorna un tablero nuevo con las jugadas que puede hacer cada jugador
    tablero2=copiar_tablero(tablero)
    for x,y in obt_jugadas_validas(tablero2,pieza):
        tablero2[x][y] = 'X'
    return tablero2

def copiar_tablero(tablero):
    #asd
    return False
def obt_jugadas_validas(tablero,pieza):
    jugadas_validas=[]
    for x in range(len(tablero[0])):
        for y in range(len(tablero[0])):
            if movimiento_esvalido(tablero,pieza,x,y)!=False:
                jugadas_validas.append([x,y])
    return jugadas_validas
def puntajes(tablero):
    blancas=0
    negras=0
    for x in range(tablero[0]):
        for y in range(tablero[0]):
            if tablero[x][y]==1:
                blancas+=1
            elif tablero[x][y]==2:
                negras+=1
    return {'Blancas':blancas,'Negras':negras}


"""
Funciones relevantes a la interfaz y generación de menú
"""
pygame.init()


flags= pygame.RESIZABLE
screen = pygame.display.set_mode((800,600),flags)
pygame.display.set_caption("Reversi")

clock = pygame.time.Clock()


def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((128, 128, 128))  # Green background
        ##Reloj
        # Get the current time
        current_time = pygame.time.get_ticks() // 1000

        # Create a font object
        font = pygame.font.Font(None, pygame.display.Info().current_w//22)

        # Render the time as text
        time_text = font.render(f"Time: {current_time}", True, (255, 255, 255))

        # Get the text's rectangle and center it at the top of the screen
        text_rect = time_text.get_rect(center=(pygame.display.Info().current_w // 2, 60))

        # Draw the time text on the screen
        screen.blit(time_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
