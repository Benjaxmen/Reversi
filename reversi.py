import tkinter as tk
from tkinter import simpledialog
import random
import threading
import time
import os
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
    if tablero[xstart][ystart] == 1 or tablero[xstart][ystart]==2 or not esta_en_tablero(tablero,xstart,ystart):
        return False
    tablero[xstart][ystart] = pieza#se agrega como placeholder esta pieza
    if pieza == 1:
        otrapieza=2
    else:
        otrapieza=1
    #se establece una lista de piezas a girar si es que se toma el movimiento
    piezas_giradas=[]
    #se recorre en las 8 direcciones posibles de la ficha para comprobar si hay fichas del otro color que se puedan dar vuetla
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y= xstart,ystart
        x+=xdirection #primer paso en la direccion
        y+=ydirection
        if esta_en_tablero(tablero,x,y) and tablero[x][y] == otrapieza:
            #hay una pieza del jugador contrario a nuestra pieza
            x+=xdirection
            y+=ydirection
            if not esta_en_tablero(tablero,x,y):
                #si no esta en tablero, se salta esta iteracion
                continue
            while tablero[x][y] == otrapieza:
                #Se "saltan" las fichas del enemigo
                x+=xdirection
                y+=ydirection
                if not esta_en_tablero(tablero,x,y):
                    break
            if not esta_en_tablero(tablero,x,y):
                continue
            #si se pilla una ficha propia en este camino, se empiezan a voltear las piezas enemigas entre estos dos puntos de forma inversa
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
 
def tablero_jugadas(tablero,tablero2,pieza):
    #retorna un tablero nuevo con las jugadas que puede hacer cada jugador
    for a in range(len(tablero[0])):
        for b in range(len(tablero[0])):
            tablero2[a][b]=0

    for x,y in obt_jugadas_validas(tablero,pieza):
        tablero2[x][y] = 'X'
    return tablero2

def copiar_tablero(tablero):
    #se hace una copia del tablero
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
    #se comprueban todos los espacios disponibles y se retorna una lista de jugadas validas
    jugadas_validas=[]
    for x in range(len(tablero[0])):
        for y in range(len(tablero[0])):
            if movimiento_esvalido(tablero,pieza,x,y)!=False:
                jugadas_validas.append([x,y])
    return jugadas_validas
def puntajes(tablero):
    #recuenta todas las fichas del tablero
    blancas=0
    negras=0
    for x in range(len(tablero[0])):
        for y in range(len(tablero[0])):
            if tablero[x][y]==1:
                blancas+=1
            elif tablero[x][y]==2:
                negras+=1
    return [blancas,negras]
class Jugador:
    def __init__(self):
        self.color = None
        self.puntaje = None

    def fichaBlanca(self):
        self.color=1
           
    def fichaNegra(self):
        self.color=2 
    
    def elegir_color(self):
        #botones para elegir la ficha
        colorF=tk.Tk()
        colorF.geometry("200x150")
        colorF.title("Elegir color de Ficha")
        titulo=tk.Label(colorF,text="ELEGIR COLOR DE FICHA",fg="black")
        titulo.pack(padx=10,pady=10,ipadx=10,ipady=10)
        tk.Button(colorF,text="Ficha Negra", command= self.fichaNegra).pack()
        tk.Button(colorF,text="Ficha Blanca",command= self.fichaBlanca).pack()

    @staticmethod
    def evaluar_tablero(tablero, pieza):
        #se ve el puntaje neto del tablero, si es favorable o no
        contadores = puntajes(tablero)
        if pieza == 1:
            return contadores[0] - contadores[1]
        else:
            return contadores[1] - contadores[0]
    
    def jugada(self, tablero, x, y):
        # se realiza una jugada y se devuelve un tablero del estado anterior a esta
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
        #se establece una jugada para el enemigo dificil
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
    def alphabeta(tablero, profundidad, alpha, beta, maximizando, pieza, nodos_explorados):
        #se realiza la poda alphabeta y contamos nodos
        nodos_explorados[0] += 1
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
                eval = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, False, pieza, nodos_explorados)
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
                eval = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, True, pieza, nodos_explorados)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def jugada_alpha_beta(self, tablero, pieza,dif):
        #se realiza la jugada elegida por alphabeta
        jugadas = obt_jugadas_validas(tablero, pieza)
        mejor_jugada = None
        mejor_evaluacion = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        profundidad = dif  # Ajusta la profundidad de búsqueda según lo desees
        
        nodos_explorados = [0]
        start_time = time.time()

        for x, y in jugadas:
            copia = copiar_tablero(tablero)
            movimiento = movimiento_esvalido(copia, pieza, x, y)
            for pieza_girada in movimiento:
                copia[pieza_girada[0]][pieza_girada[1]] = pieza
            copia[x][y] = pieza
            evaluacion = Jugador.alphabeta(copia, profundidad - 1, alpha, beta, False, pieza, nodos_explorados)
            if evaluacion > mejor_evaluacion:
                mejor_evaluacion = evaluacion
                mejor_jugada = (x, y)
            alpha = max(alpha, evaluacion)
        end_time = time.time()
        tiempo_total = end_time - start_time
        tiempo_total=str(tiempo_total).replace('.',',')
        print(f"Nodos explorados: {nodos_explorados[0]}")
        print(f"Tiempo utilizado: {tiempo_total} segundos")

        return mejor_jugada




"""
Aqui van las funciones necesarias para poder hacer una interfaz gráfica
"""
class Reversi:
    
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.root=tk.Tk()
        self.total=4
        self.dif = tk.Tk()
        self.dif.title("Dificultad:")
        self.root.title("Reversi Game")
        self.dificultad=0
        self.sugerencia=0
        self.vacio = tk.PhotoImage(file=os.path.join(script_dir, "alt", "vacio.png"))
        self.blanca = tk.PhotoImage(file=os.path.join(script_dir, "alt", "blanca.png"))
        self.negra = tk.PhotoImage(file=os.path.join(script_dir, "alt", "negra.png"))
        self.sugerencias = tk.PhotoImage(file=os.path.join(script_dir, "alt", "sugerencia.png"))
        self.posible = tk.PhotoImage(file=os.path.join(script_dir, "alt", "posible.png"))

        self.board_size = None
        self.tablero = None
        self.tablero_anterior = None  # Variable para guardar el tablero anterior
        self.posibles_jugadas=None

        self.jugador = Jugador()
        self.jugador.elegir_color()  # El jugador elige su color
        self.enemigo=Jugador()

        self.create_ui()
        self.seleccion_dif()
        self.root.mainloop()

    def start_game(self, board_size):
        #se elige el tamaño del tablero y los colores, junto a la eleccion de quien parte
        if board_size == 6:
            self.board_size = 6
            self.tablero = generar_tablero_6()
            self.posibles_jugadas=generar_tablero_6()
            reiniciar_tablero_6(self.tablero)

        elif board_size == 8:
            self.board_size = 8
            self.tablero = generar_tablero_8()
            self.posibles_jugadas=generar_tablero_8()
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
        #se establece el tablero, se ven los puntajes y casi todo el funcionamiento del juego de forma gráfica
        #esta es la funcion principal que dibuja todas las celdas y los botones correspondientes
        self.clear_frame(self.root)
        puntaje=tk.Frame(self.root,bg='light gray')
        puntaje.pack()
        contadores=puntajes(self.tablero)
        tablero_jugadas(self.tablero,self.posibles_jugadas,self.jugador.color)
        if self.sugerencia==1:
            jugada = self.jugador.jugada_alpha_beta(self.tablero, self.jugador.color,20)
            self.posibles_jugadas[jugada[0]][jugada[1]]="S"
        if (self.total)==self.board_size**2:
            fin=tk.Tk()
            if (contadores[self.jugador.color-1]>contadores[self.enemigo.color-1]):
                fin.title("Ganaste!")
                etiqueta=tk.Label(fin,text='Le ganaste a la computadora!')
                etiqueta.pack()
            elif (contadores[self.jugador.color-1]<contadores[self.enemigo.color-1]):
                fin.title("Perdiste!")
                etiqueta=tk.Label(fin,text='La computadora te ganó!')
                etiqueta.pack()
            else:
                fin.title("Empate!")
                etiqueta=tk.Label(fin,text='Empataste con la computadora!')
                etiqueta.pack()

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
                elif self.posibles_jugadas[i][j] == 'S':
                    cell_button.config(image=self.sugerencias)
                elif self.posibles_jugadas[i][j] == 'X':
                    cell_button.config(image=self.posible)
                    
                else:
                    cell_button.config(image=self.vacio)
        self.sugerencia=0

        # Agrega el botón de deshacer en un marco separado
        undo_frame = tk.Frame(frame)
        undo_frame.pack()
        button_undo = tk.Button(undo_frame, text="Deshacer", command=self.undo_move)
        button_undo.pack()
        button_suggestion=tk.Button(undo_frame, text="Sugerencias",command=self.mostrar_jugadas)
        button_suggestion.pack()
        button_pass=tk.Button(undo_frame,text="Pasar",command=self.pasar)
        button_pass.pack()
    def pasar(self):
        #se deja que el enemigo juegue nuevamente
        threading.Timer(1.0,self.jugada_enemiga).start()
        self.mostrar_tablero()  
        contadores=puntajes(self.tablero)
        if not obt_jugadas_validas(self.tablero,self.jugador.color)and not obt_jugadas_validas(self.tablero,self.enemigo.color) and  (self.total)!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            if contadores[self.jugador.color-1]>contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganaste!.')
                etiqueta.pack()
            elif contadores[self.jugador.color-1]<contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganó la computadora!.')
                etiqueta.pack()
            else:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero empataste!.')
                etiqueta.pack()
            return
        if not obt_jugadas_validas(self.tablero,self.enemigo.color) and (self.total)!=self.board_size**2 :
            sin_jugadas=tk.Tk()
            sin_jugadas.title("Pasa el turno!")
            etiqueta=tk.Label(sin_jugadas,text='Tu oponente se quedó sin jugadas, vuelve a jugar!')
            etiqueta.pack()
            
        
        elif not obt_jugadas_validas(self.tablero, self.jugador.color) and (self.total)!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            etiqueta = tk.Label(mensaje, text='No tienes movimientos válidos, pasa tu turno.')
            etiqueta.pack()
    def mostrar_jugadas(self):
        #se realiza un cambio para que en mostrar_tablero muestre una jugada hecha por la poda alphabeta
        self.sugerencia=1
        self.mostrar_tablero()
    def handle_click(self, x, y):
        #se realizan las jugadas por el boton presionado, tomando en cuenta la posicion de este
        jugada_posible=self.jugador.jugada(self.tablero, x, y)
        if jugada_posible==False:
            inv=tk.Tk()
            inv.title("Movimiento Inválido!")
            etiqueta=tk.Label(inv,text='Movimiento inválido, intenta nuevamente!')
            etiqueta.pack()
            return False
        self.tablero_anterior=jugada_posible
        self.total+=1
        self.mostrar_tablero()  # Asegúrate de llamar a mostrar_tablero después de cada jugada válida
        contadores=puntajes(self.tablero)
        if not obt_jugadas_validas(self.tablero,self.enemigo.color) and (self.total)!=self.board_size**2 :
            sin_jugadas=tk.Tk()
            sin_jugadas.title("Pasa el turno!")
            etiqueta=tk.Label(sin_jugadas,text='Tu oponente se quedó sin jugadas, vuelve a jugar!')
            etiqueta.pack()
            return
        threading.Timer(1.0,self.jugada_enemiga).start()
        contadores=puntajes(self.tablero)
        if not obt_jugadas_validas(self.tablero,self.jugador.color)and not obt_jugadas_validas(self.tablero,self.enemigo.color) and  (self.total)!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            if contadores[self.jugador.color-1]>contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganaste!.')
                etiqueta.pack()
            elif contadores[self.jugador.color-1]<contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganó la computadora!.')
                etiqueta.pack()
            else:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero empataste!.')
                etiqueta.pack()
        elif not obt_jugadas_validas(self.tablero, self.jugador.color) and (self.total)!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            etiqueta = tk.Label(mensaje, text='No tienes movimientos válidos, pasa tu turno.')
            etiqueta.pack()
        





    def clear_frame(self, frame):
        #reinicia el tablero
        for widget in frame.winfo_children():
            widget.destroy()
    def create_ui(self):
        #inicializa el tablero
        label = tk.Label(self.root, text="Selecciona el tamaño del tablero:")
        label.pack(pady=10)

        button_6x6 = tk.Button(self.root, text="6x6", command=lambda: self.start_game(6))
        button_6x6.pack()

        button_8x8 = tk.Button(self.root, text="8x8", command=lambda: self.start_game(8))
        button_8x8.pack()
    def seleccion_dif(self):
        #se elige la dificultad
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
        #se rescata el tablero anterior a la jugada
        if self.tablero_anterior is not None:
            self.tablero = self.tablero_anterior
            self.tablero_anterior = None
            self.total-=1
            self.mostrar_tablero()
    def jugada_enemiga(self):
        #se realiza el movimiento enemigo considerando la dificultad enemiga
        if self.dificultad==0:   
            jugadas=obt_jugadas_validas(self.tablero,self.enemigo.color)
            if len(jugadas)>0:
                jugada=random.choice(jugadas)
                self.enemigo.jugada(self.tablero,jugada[0],jugada[1])
                self.mostrar_tablero()
        
                      
        elif self.dificultad==1:
            jugada = self.enemigo.jugada_alpha_beta(self.tablero, self.enemigo.color,6)
            if jugada is not None:
                x, y = jugada
                self.enemigo.jugada_dificil(self.tablero, x, y, self.enemigo.color)
                self.mostrar_tablero()
        
        elif self.dificultad==2:
            jugada = self.enemigo.jugada_alpha_beta(self.tablero, self.enemigo.color,20)
            if jugada is not None:
                x, y = jugada
                self.enemigo.jugada_dificil(self.tablero, x, y, self.enemigo.color)
                self.mostrar_tablero()
        contadores=puntajes(self.tablero)
        self.total+=1
        if not obt_jugadas_validas(self.tablero,self.jugador.color)and not obt_jugadas_validas(self.tablero,self.enemigo.color) and  (contadores[0]+contadores[1])!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            if contadores[self.jugador.color-1]>contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganaste!.')
                etiqueta.pack()
            elif contadores[self.jugador.color-1]<contadores[self.enemigo.color-1]:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero ganó la computadora!.')
                etiqueta.pack()
            else:
                etiqueta = tk.Label(mensaje, text='Nadie tiene movimientos válidos, pero empataste!.')
                etiqueta.pack()
        elif not obt_jugadas_validas(self.tablero, self.jugador.color) and (contadores[0]+contadores[1])!=self.board_size**2:
            mensaje = tk.Tk()
            mensaje.title("Sin movimientos válidos")
            etiqueta = tk.Label(mensaje, text='No tienes movimientos válidos, pasa tu turno.')
            etiqueta.pack()
        if (contadores[0]+contadores[1])==self.board_size**2:
            fin=tk.Tk()
            if (contadores[self.jugador.color-1]>contadores[self.enemigo.color-1]):
                fin.title("Ganaste!")
                etiqueta=tk.Label(fin,text='Le ganaste a la computadora!')
                etiqueta.pack()
            elif (contadores[self.jugador.color-1]<contadores[self.enemigo.color-1]):
                fin.title("Perdiste!")
                etiqueta=tk.Label(fin,text='La computadora te ganó!')
                etiqueta.pack()
            else:
                fin.title("Empate!")
                etiqueta=tk.Label(fin,text='Empataste con la computadora!')
                etiqueta.pack()



if __name__ == "__main__":
    reversi_game = Reversi()