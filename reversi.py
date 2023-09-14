import tkinter as tk
from tkinter import simpledialog
import random
import time
import threading
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

    @staticmethod
    def evaluar_tablero(tablero, pieza):
        contadores = puntajes(tablero)
        if pieza == 1:
            return contadores[0] - contadores[1]
        else:
            return contadores[1] - contadores[0]
    
    def jugada(self, tablero, x, y):
        movimiento = movimiento_esvalido(tablero, self.color, x, y)
        if movimiento == False:
            return False
        copia = copiar_tablero(tablero)
        if movimiento is not False:
            self.tablero_anterior = copia
            for pieza in movimiento:
                tablero[pieza[0]][pieza[1]] = self.color
            tablero[x][y]=self.color
            return copia
    def jugada_dificil(self, tablero, x, y, color):
        movimiento = movimiento_esvalido(tablero, color, x, y)
        copia = copiar_tablero(tablero)

        if movimiento is not False:
            self.tablero_anterior = copia
            for pieza in movimiento:
                tablero[pieza[0]][pieza[1]] = color
            tablero[x][y] = color
            return copia
        else:
            self.jugada(self,tablero, x, y, color)
    @staticmethod
    def alphabeta(tablero, profundidad, alpha, beta, maximizando, pieza):
        if profundidad == 0 or len(obt_jugadas_validas(tablero, pieza)) == 0:
            return Jugador.evaluar_tablero(tablero, pieza)

        if maximizando:
            max_eval = float('-inf')
            for x, y in obt_jugadas_validas(tablero, pieza):
                copia = copiar_tablero(tablero)
                movimiento = movimiento_esvalido(copia, pieza, x, y)
                for pieza_girada in movimiento:
                    copia[pieza_girada[0]][pieza_girada[1]] = pieza
                copia[x][y] = pieza
                eval = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, False, pieza)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for x, y in obt_jugadas_validas(tablero, pieza):
                copia = copiar_tablero(tablero)
                movimiento = movimiento_esvalido(copia, pieza, x, y)
                for pieza_girada in movimiento:
                    copia[pieza_girada[0]][pieza_girada[1]] = pieza
                copia[x][y] = pieza
                eval = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, True, pieza)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def jugada_alpha_beta(self, tablero, pieza):
        jugadas = obt_jugadas_validas(tablero, pieza)
        mejor_jugada = None
        mejor_evaluacion = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        profundidad = 4  # Ajusta la profundidad de búsqueda según lo desees

        for x, y in jugadas:
            copia = copiar_tablero(tablero)
            movimiento = movimiento_esvalido(copia, pieza, x, y)
            for pieza_girada in movimiento:
                copia[pieza_girada[0]][pieza_girada[1]] = pieza
            copia[x][y] = pieza
            evaluacion = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, False, pieza)
            if evaluacion > mejor_evaluacion:
                mejor_evaluacion = evaluacion
                mejor_jugada = (x, y)
            alpha = max(alpha, evaluacion)

        return mejor_jugada




"""
Aqui van las funciones necesarias para poder hacer una interfaz gráfica
"""
class Reversi:
    
    def __init__(self):
        self.root=tk.Tk()
        self.dif = tk.Tk()
        self.dif.title("Dificultad:")
        self.root.title("Reversi Game")
        self.dificultad=0

        self.vacio = tk.PhotoImage(file="./alt/vacio.png")
        self.blanca = tk.PhotoImage(file="./alt/blanca.png")
        self.negra = tk.PhotoImage(file="./alt/negra.png")
        self.sugerencia = tk.PhotoImage(file="./alt/posible.png")

        self.board_size = None
        self.tablero = None
        self.tablero_anterior = None  # Variable para guardar el tablero anterior

        self.jugador = Jugador()
        self.jugador.elegir_color()  # El jugador elige su color
        self.enemigo=Jugador()

        self.create_ui()
        self.seleccion_dif()
        self.root.mainloop()

    def start_game(self, board_size):
        
        if board_size == 6:
            self.board_size = 6
            self.tablero = generar_tablero_6()
            reiniciar_tablero_6(self.tablero)

        elif board_size == 8:
            self.board_size = 8
            self.tablero = generar_tablero_8()
            reiniciar_tablero_8(self.tablero)
        self.mostrar_tablero()
        parte=random.choice([1,2])
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
            self.jugada_enemiga()

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
                cell_button = tk.Button(fila_frame, width=80, height=80, relief="ridge", state=tk.ACTIVE,
                                       command=lambda x=i, y=j: self.handle_click(x, y))
                cell_button.grid(row=i, column=j)

                if valor == 1:
                    cell_button.config(image=self.blanca)
                elif valor == 2:
                    cell_button.config(image=self.negra)
                elif valor == 'X':
                    cell_button.config(image=self.sugerencia)
                    
                else:
                    cell_button.config(image=self.vacio)
                    

        # Agrega el botón de deshacer en un marco separado
        undo_frame = tk.Frame(frame)
        undo_frame.pack()
        button_undo = tk.Button(undo_frame, text="Deshacer", command=self.undo_move)
        button_undo.pack()
        button_suggestion=tk.Button(undo_frame, text="Sugerencias",command=self.mostrar_jugadas)
        button_suggestion.pack()
    def handle_click(self, x, y):
        
        jugada_posible=self.jugador.jugada(self.tablero, x, y)
        if jugada_posible==False:
            inv=tk.Tk()
            inv.title("Movimiento Inválido!")
            etiqueta=tk.Label(inv,text='Movimiento inválido, intenta nuevamente!')
            etiqueta.pack()
            return False
        self.tablero_anterior=jugada_posible
        copia_sin_sug(self.tablero)
        self.mostrar_tablero()  # Asegúrate de llamar a mostrar_tablero después de cada jugada válida
        threading.Timer(1.0,self.jugada_enemiga).start()

        
        
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
    def seleccion_dif(self):
        label = tk.Label(self.dif, text="Selecciona la dificultad del bot:")
        label.pack(pady=10)

        button_easy = tk.Button(self.dif, text="Fácil", command=lambda: self.dificultad_elegir(0))
        button_easy.pack()

        button_medium = tk.Button(self.dif, text="Normal", command=lambda: self.dificultad_elegir(1))
        button_medium.pack()
        button_hard = tk.Button(self.dif, text="Dificil", command=lambda: self.dificultad_elegir(2))
        button_hard.pack()
    def dificultad_elegir(self,num):
        self.dificultad=num
        return False

    def undo_move(self):
        if self.tablero_anterior is not None:
            self.tablero = self.tablero_anterior
            self.tablero_anterior = None
            self.mostrar_tablero()
    def jugada_enemiga(self):
        if self.dificultad==0:   
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
        elif self.dificultad==2:
            jugada = self.enemigo.jugada_alpha_beta(self.tablero, self.enemigo.color)
            if jugada is not None:
                x, y = jugada
                self.enemigo.jugada_dificil(self.tablero, x, y, self.enemigo.color)
                self.mostrar_tablero()
            else:
                ganaste = tk.Tk()
                ganaste.title("Ganaste!")
                etiqueta = tk.Label(ganaste, text='Le ganaste a la computadora!')
                etiqueta.pack()


if __name__ == "__main__":
    reversi_game = Reversi()