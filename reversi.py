import tkinter as tk
from tkinter import simpledialog
import random
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
def copia_sin_sug(tablero):
    for x in range(len(tablero[0])):
        for y in range(len(tablero[0])):
            if tablero[x][y]=='X':
                tablero[x][y]=0
def esta_en_tablero(tablero,x,y):
    return x>=0 and len(tablero[0])>x and y>=0 and len(tablero[0])>y
def movimiento_esvalido(tablero, pieza, xstart, ystart):
    #retorna falso si la jugada es invalida o está usada la posicion
    if tablero[xstart][ystart] == 1 or tablero[xstart][ystart]==2 or not esta_en_tablero(tablero,xstart,ystart):
        return False
    tablero[xstart][ystart] = pieza#se agrega como placeholder esta pieza
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
            while tablero[x][y] == otrapieza:
                x+=xdirection
                y+=ydirection
                if not esta_en_tablero(tablero,x,y):
                    break
            if not esta_en_tablero(tablero,x,y):
                continue
            if tablero[x][y] == pieza:
                while True:
                    x-=xdirection
                    y-=ydirection
                    if x==xstart and y==ystart:
                        break
                    piezas_giradas.append([x,y])
    tablero[xstart][ystart]=0#se restaura el estado original
    if len(piezas_giradas)==0:
        return False
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
    for x in range(len(tablero[0])):
        for y in range(len(tablero[0])):
            if tablero[x][y]==1:
                blancas+=1
            elif tablero[x][y]==2:
                negras+=1
    return [blancas,negras]
def esquina(x,y,tablero):
    if len(tablero[0])==6:
        return (x==0 and y==0) or (x==5 and y==0) or (x==0 and y==5) or (x==5 and y==5)
    else:
        return (x==0 and y==0) or (x==7 and y==0) or (x==0 and y==7) or (x==7 and y==7)
class Jugador:
    def __init__(self):
        self.color = None
        self.puntaje = None

    def elegir_color(self):
        self.color = simpledialog.askinteger("Color", "Elija su color (1 para Blancas, 2 para Negras):", minvalue=1, maxvalue=2)

    def deshacer_ultima_jugada(self):
        if self.tablero_anterior is not None:
            self.tablero = self.tablero_anterior
            self.tablero_anterior=None
    def jugada(self, tablero, x, y):
        movimiento = movimiento_esvalido(tablero, self.color, x, y)
        copia = copiar_tablero(tablero)
        if movimiento is not False:
            self.tablero_anterior = copia
            for pieza in movimiento:
                tablero[pieza[0]][pieza[1]] = self.color
            tablero[x][y]=self.color
            return copia





"""
Aqui van las funciones necesarias para poder hacer una interfaz gráfica
"""
class Reversi:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reversi Game")
        self.turno = 0

        self.vacio = tk.PhotoImage(file="vacio.gif")
        self.blanca = tk.PhotoImage(file="blanca.gif")
        self.negra = tk.PhotoImage(file="negra.gif")
        self.sugerencia = tk.PhotoImage(file="sugerencia.gif")

        self.board_size = None
        self.tablero = None
        self.tablero_anterior = None  # Variable para guardar el tablero anterior

        self.jugador = Jugador()
        self.jugador.elegir_color()  # El jugador elige su color
        self.enemigo=Jugador()

        self.create_ui()
        self.root.mainloop()

    def start_game(self, board_size):
        parte=random.choice([1,2])
        self.turno=parte
        if self.jugador.color==1:
            self.enemigo.color=2
        else:
            self.enemigo.color=1
        if parte==self.jugador.color:
            partes=tk.Tk()
            partes.title("Tu partes!")
            etiqueta=tk.Label(partes,text='Haz la primera jugada!')
            etiqueta.pack()
        else:
            partes=tk.Tk()
            partes.title("Tu oponente parte!")
            etiqueta=tk.Label(partes,text='Juegas segundo!')
            etiqueta.pack()
        if board_size == 6:
            self.board_size = 6
            self.tablero = generar_tablero_6()
            reiniciar_tablero_6(self.tablero)

        elif board_size == 8:
            self.board_size = 8
            self.tablero = generar_tablero_8()
            reiniciar_tablero_8(self.tablero)
        self.mostrar_tablero()

    def mostrar_tablero(self):
        self.clear_frame(self.root)
        puntaje=tk.Frame(self.root,bg='light gray')
        puntaje.pack()
        contadores=puntajes(self.tablero)
        contador=tk.Label(puntaje,justify="center",text=f'Blancas:{contadores[0]}          Negras:{contadores[1]}')
        contador.pack()
        frame = tk.Frame(self.root, bg="light gray")
        frame.pack()
        

        for i, fila in enumerate(self.tablero):
            fila_frame = tk.Frame(frame)
            fila_frame.pack()
            for j, valor in enumerate(fila):
                cell_button = tk.Button(fila_frame, width=80, height=80, relief="ridge", state=tk.DISABLED,
                                       command=lambda x=i, y=j: self.handle_click(x, y))
                cell_button.grid(row=i, column=j)

                if valor == 1:
                    cell_button.config(image=self.blanca)
                elif valor == 2:
                    cell_button.config(image=self.negra)
                elif valor == 'X':
                    cell_button.config(image=self.sugerencia)
                    cell_button.config(state=tk.ACTIVE)
                else:
                    cell_button.config(image=self.vacio)
                    cell_button.config(state=tk.ACTIVE)

        # Agrega el botón de deshacer en un marco separado
        undo_frame = tk.Frame(frame)
        undo_frame.pack()
        button_undo = tk.Button(undo_frame, text="Deshacer", command=self.undo_move)
        button_undo.pack()
        button_suggestion=tk.Button(undo_frame, text="Sugerencias",command=self.mostrar_jugadas)
        button_suggestion.pack()

    def handle_click(self, x, y):
        self.tablero_anterior=self.jugador.jugada(self.tablero, x, y)
        copia_sin_sug(self.tablero)
        self.mostrar_tablero()  # Asegúrate de llamar a mostrar_tablero después de cada jugada válida
        self.jugada_enemiga()
        if len(obt_jugadas_validas(self.tablero,self.jugador.color))==0:
            perdiste=tk.Tk()
            perdiste.title("Perdiste!")
            etiqueta=tk.Label(perdiste,text='Te ganó la computadora!')
            etiqueta.pack()

    def mostrar_jugadas(self):
        self.tablero=tablero_jugadas(self.tablero,self.jugador.color)
        self.mostrar_tablero()


    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    def create_ui(self):
        label = tk.Label(self.root, text="Selecciona el tamaño del tablero:")
        label.pack(pady=10)

        button_6x6 = tk.Button(self.root, text="6x6", command=lambda: self.start_game(6))
        button_6x6.pack()

        button_8x8 = tk.Button(self.root, text="8x8", command=lambda: self.start_game(8))
        button_8x8.pack()
        
    def undo_move(self):
        if self.tablero_anterior is not None:
            self.tablero = self.tablero_anterior
            self.tablero_anterior = None
            self.mostrar_tablero()
    def jugada_enemiga(self):
        jugadas=obt_jugadas_validas(self.tablero,self.enemigo.color)
        if len(jugadas)>0:
            jugada=random.choice(jugadas)
            self.enemigo.jugada(self.tablero,jugada[0],jugada[1])
            self.mostrar_tablero()
        else:
            ganaste=tk.Tk()
            ganaste.title("Ganaste!")
            etiqueta=tk.Label(ganaste,text='Le ganaste a la computadora!')
            etiqueta.pack()
        


if __name__ == "__main__":
    reversi_game = Reversi()