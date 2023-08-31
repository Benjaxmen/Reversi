import sys
import tkinter as tk
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
    if len(tablero[0])==8:
        tablero2=generar_tablero_8()
        for x in range(8):
            for y in range(8):
                tablero2[x][y]=tablero[x][y]
    else:
        tablero2=generar_tablero_6()
        for x in range(6):
            for y in range(6):
                tablero2[x][y]=tablero[x][y]

    return tablero2
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
Aqui van las funciones necesarias para poder hacer una interfaz gráfica
"""
def start_game(board_size):
    if board_size == 6:
        tablero = generar_tablero_6()
        reiniciar_tablero_6(tablero)
        tablero[1][0] = 'X'
    elif board_size == 8:
        tablero = generar_tablero_8()
        reiniciar_tablero_8(tablero)
        tablero[1][0] = 'X'
    mostrar_tablero(tablero)

def mostrar_tablero(tablero):
    root = tk.Tk()
    root.title("Tablero de Reversi")

    frame = tk.Frame(root, bg="light gray")
    frame.pack()

    for i, fila in enumerate(tablero):
        fila_frame = tk.Frame(frame)
        fila_frame.pack()
        for j, valor in enumerate(fila):
            # Crear un botón para cada casilla
            cell_button = tk.Button(fila_frame, width=80, height=80, relief="ridge", state=tk.DISABLED)  # Desactivar el clic
            cell_button.grid(row=i, column=j)
            
            # Configurar el contenido del botón según el valor en el tablero
            if valor == 1:
                ficha = tk.PhotoImage(file="blanca.gif")  # Ruta a tu imagen blanca
                cell_button.config(image=ficha)
            elif valor == 2:
                ficha = tk.PhotoImage(file="negra.gif")  # Ruta a tu imagen negra
                cell_button.config(image=ficha)
            elif valor == 'X':
                sugerencia=tk.PhotoImage(file="sugerencia.gif")
                cell_button.config(image=sugerencia)


    root.mainloop()

def create_ui():
    root = tk.Tk()
    root.title("Reversi Game")

    label = tk.Label(root, text="Selecciona el tamaño del tablero:")
    label.pack(pady=10)

    button_6x6 = tk.Button(root, text="6x6", command=lambda: start_game(6))
    button_6x6.pack()

    button_8x8 = tk.Button(root, text="8x8", command=lambda: start_game(8))
    button_8x8.pack()

    root.mainloop()

if __name__ == "__main__":
    create_ui()