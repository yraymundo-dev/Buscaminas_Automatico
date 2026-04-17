import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class BuscaminasExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Buscaminas")
        self.filas = 10
        self.columnas = 10
        
        # Tablero de la IA (None: oculto, 'M': mina, número int: revelado)
        self.tablero_ia = [[None for _ in range(10)] for _ in range(10)]
        self.botones = [[None for _ in range(10)] for _ in range(10)]
        
        self.crear_interfaz()
        self.root.after(1000, self.iniciar_juego)

    def crear_interfaz(self):
        for r in range(self.filas):
            for c in range(self.columnas):
                btn = tk.Button(self.root, text="", width=4, height=2, bg="#d1d1d1", font=('Arial', 10, 'bold'))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.botones[r][c] = btn

    def obtener_vecinos(self, r, c):
        vecinos = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.filas and 0 <= nc < self.columnas:
                        vecinos.append((nr, nc))
        return vecinos

    def iniciar_juego(self):
        # Escoger una primera casilla al azar
        r, c = random.randint(0, 9), random.randint(0, 9)
        self.pedir_dato(r, c, "Primer movimiento (Seguro)")

    def pedir_dato(self, r, c, motivo):
        self.botones[r][c].config(bg="#80d8ff") # Iluminar azul para seleccionada
        self.root.update()
        
        # Analizar los vecinos de esta casilla para recomendar valores
        vecinos = self.obtener_vecinos(r, c)
        flags = sum(1 for vr, vc in vecinos if self.tablero_ia[vr][vc] == 'M')
        ocultos = sum(1 for vr, vc in vecinos if self.tablero_ia[vr][vc] is None)
        
        min_val = flags                 # Lo mínimo es la cantidad de minas ya marcadas
        max_val = flags + ocultos       # Lo máximo es si todas las ocultas fueran minas
        
        if min_val == max_val:
            # Si solo hay una opción lógica, lo rellenamos automáticamente
            num = min_val
        else:
            # Mostramos al usuario una recomendación clara sin errores imposibles
            num = simpledialog.askinteger(
                "Ingreso IA", 
                f"Motivo: {motivo}\n\n"
                f"Casilla: ({r}, {c})\n"
                f"Para esta casilla, el valor LÓGICO DEBE ESTAR ENTRE {min_val} y {max_val}.\n\n"
                f"¿Cuántas minas ves alrededor?"
            )
            
        # Si el usuario cierra el cuadro en la "X"
        if num is None:
            self.root.destroy()
            return
            
        # Nueva comprobación de errores simple: obligar a que ponga un dato de los recomendados
        if not (min_val <= num <= max_val):
            messagebox.showerror("Error", f"Valor incorrecto. Debe estar obligatoriamente entre {min_val} y {max_val}.")
            self.botones[r][c].config(bg="#d1d1d1")
            self.root.after(300, lambda: self.pedir_dato(r, c, motivo))
            return
            
        # Guardamos en la memoria de la IA
        self.tablero_ia[r][c] = num
        self.botones[r][c].config(text=str(num), bg="#ffffff", relief="sunken", fg="black")
        
        # Regla de barrido automático del buscaminas: cuando sale un "0" se destapan los vecinos
        if num == 0:
            for vr, vc in vecinos:
                if self.tablero_ia[vr][vc] is None:
                    self.tablero_ia[vr][vc] = 0
                    self.botones[vr][vc].config(text="0", bg="#ffffff", relief="sunken")
                    
        self.analizar_tablero()

    def analizar_tablero(self):
        # 1. Bucle para marcar todas las minas que sean evidentes (certezas)
        hubo_cambio = True
        while hubo_cambio:
            hubo_cambio = False
            for r in range(self.filas):
                for c in range(self.columnas):
                    val = self.tablero_ia[r][c]
                    if isinstance(val, int):
                        vecinos = self.obtener_vecinos(r, c)
                        flags = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] == 'M']
                        ocultos = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] is None]
                        
                        # Si (ocultos + banderas) = valor de la celda, los ocultos restantes SOM MINAS
                        if len(ocultos) + len(flags) == val and len(ocultos) > 0:
                            for vr, vc in ocultos:
                                self.tablero_ia[vr][vc] = 'M'
                                self.botones[vr][vc].config(text="🚩", bg="#ffadad", fg="black")
                            hubo_cambio = True

        # 2. Buscar casillas que sean 100% seguras para destapar ahora
        for r in range(self.filas):
            for c in range(self.columnas):
                val = self.tablero_ia[r][c]
                if isinstance(val, int):
                    vecinos = self.obtener_vecinos(r, c)
                    flags = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] == 'M']
                    ocultos = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] is None]
                    
                    # Si ya tengo todas las banderas listas para un número, los otros ocultos son seguros
                    if len(flags) == val and len(ocultos) > 0:
                        self.pedir_dato(ocultos[0][0], ocultos[0][1], "Casilla 100% Segura")
                        return

        # 3. Si no hay celdas lógicas, aplicar cálculo probabilístico básico
        riesgos = {}
        for r in range(self.filas):
            for c in range(self.columnas):
                if self.tablero_ia[r][c] is None:
                    riesgo_acumulado = 0.0
                    vecinos = self.obtener_vecinos(r, c)
                    
                    for vr, vc in vecinos:
                        val = self.tablero_ia[vr][vc]
                        if isinstance(val, int) and val > 0:
                            vvecinos = self.obtener_vecinos(vr, vc)
                            vflags = sum(1 for x, y in vvecinos if self.tablero_ia[x][y] == 'M')
                            vocultos = sum(1 for x, y in vvecinos if self.tablero_ia[x][y] is None)
                            
                            # Si faltan minas por cubrir en esa casilla
                            if val > vflags and vocultos > 0:
                                riesgo_acumulado += (val - vflags) / vocultos
                    # Agregamos riesgo al dict sumatorio para evaluar qué celda usar
                    riesgos[(r, c)] = riesgo_acumulado
        
        # Evaluar la celda oculta calculada más segura
        if riesgos:
            # Quedarnos con el valor de la lista dictado del algoritmo
            mejor_casilla = min(riesgos, key=riesgos.get)
            min_riesgo = riesgos[mejor_casilla]
            self.pedir_dato(mejor_casilla[0], mejor_casilla[1], f"Probabilidad, Riesgo: {min_riesgo:.2f}")
        else:
            messagebox.showinfo("Fin del Análisis", "No quedan más casillas que analizar o el tablero está completo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuscaminasExperto(root)
    root.mainloop()