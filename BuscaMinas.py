import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class BuscaminasExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Buscaminas: Simulador de Pensamiento Humano")
        self.filas = 10
        self.columnas = 10
        
        # Tablero interno (None: oculto, 'M': mina deducida, int: número)
        self.tablero_ia = [[None for _ in range(10)] for _ in range(10)]
        self.botones = [[None for _ in range(10)] for _ in range(10)]
        
        self.crear_interfaz()
        # Pequeña pausa para que cargue la ventana antes de pedir el primer dato
        self.root.after(1000, self.iniciar_juego)

    def crear_interfaz(self):
        for r in range(self.filas):
            for c in range(self.columnas):
                btn = tk.Button(self.root, text="", width=4, height=2, 
                                bg="#d1d1d1", font=('Arial', 10, 'bold'),
                                relief="raised")
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.botones[r][c] = btn

    def obtener_vecinos(self, r, c):
        return [(r+dr, c+dc) for dr in [-1,0,1] for dc in [-1,0,1]
                if (dr!=0 or dc!=0) and 0<=r+dr<10 and 0<=c+dc<10]

    def iniciar_juego(self):
        # PRIMER MOVIMIENTO: Aleatorio total
        r, c = random.randint(0, 9), random.randint(0, 9)
        self.procesar_movimiento(r, c, "Primer movimiento (Azar)")

    def calcular_probabilidades(self):
        riesgo = {}
        disponibles = [(r, c) for r in range(10) for c in range(10) if self.tablero_ia[r][c] is None]
        
        for r, c in disponibles:
            riesgo[(r, c)] = 0.0
            for vr, vc in self.obtener_vecinos(r, c):
                val = self.tablero_ia[vr][vc]
                if isinstance(val, int) and val > 0:
                    v_vecinos = self.obtener_vecinos(vr, vc)
                    v_ocultos = [v for v in v_vecinos if self.tablero_ia[v[0]][v[1]] is None]
                    v_flags = [v for v in v_vecinos if self.tablero_ia[v[0]][v[1]] == 'M']
                    
                    minas_restantes = val - len(v_flags)
                    if len(v_ocultos) > 0:
                        riesgo[(r, c)] += minas_restantes / len(v_ocultos)
        return riesgo

    def analizar_siguiente_paso(self):
        # 1. Buscar Certezas (Lógica de bandera y limpieza)
        for r in range(10):
            for c in range(10):
                val = self.tablero_ia[r][c]
                if isinstance(val, int) and val > 0:
                    vecinos = self.obtener_vecinos(r, c)
                    ocultos = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] is None]
                    flags = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] == 'M']
                    
                    if len(ocultos) + len(flags) == val:
                        for vr, vc in ocultos:
                            self.tablero_ia[vr][vc] = 'M'
                            self.botones[vr][vc].config(text="🚩", bg="#ffadad", fg="black")
                    
                    if len(flags) == val and len(ocultos) > 0:
                        return ocultos[0], "Deducción Lógica (Seguro)"

        # 2. Probabilidad si no hay certezas
        riesgos = self.calcular_probabilidades()
        if riesgos:
            mejor = min(riesgos, key=riesgos.get)
            return mejor, f"Análisis Probabilístico (Riesgo: {riesgos[mejor]:.2f})"
        
        return None, None

    def procesar_movimiento(self, r, c, motivo):
        self.botones[r][c].config(bg="#80d8ff") # Resaltar elección
        self.root.update()
        
        num = simpledialog.askinteger("IA Decidiendo", 
                                      f"Motivo: {motivo}\n\nElegí la casilla ({r}, {c})\n¿Cuántas minas ves alrededor?")
        
        if num is not None:
            # Validaciones de integridad
            vecinos = self.obtener_vecinos(r, c)
            ocultos_reales = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] != 'M']
            
            if num > len(vecinos):
                messagebox.showerror("Error", "Dato imposible. Supera el número de vecinos.")
            else:
                self.tablero_ia[r][c] = num
                self.botones[r][c].config(text=str(num), bg="#ffffff", relief="sunken")
                
                # Gestión del 0 (Expansión automática humana)
                if num == 0:
                    for nr, nc in vecinos:
                        if self.tablero_ia[nr][nc] is None:
                            self.tablero_ia[nr][nc] = 0
                            self.botones[nr][nc].config(text="0", bg="#ffffff", relief="sunken")

            # Buscar siguiente movimiento
            prox_coord, prox_motivo = self.analizar_siguiente_paso()
            if prox_coord:
                self.root.after(500, lambda: self.procesar_movimiento(prox_coord[0], prox_coord[1], prox_motivo))
            else:
                messagebox.showinfo("Victoria", "Ya no quedan casillas por deducir.")
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BuscaminasExperto(root)
    root.mainloop()