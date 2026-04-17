import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class DialogoPC(tk.Toplevel):
    def __init__(self, parent, r, c, motivo, valores_posibles, permite_mina):
        super().__init__(parent)
        self.title("Turno de la Máquina (Tú)")
        
        # Posicionar paralela a la principal
        parent.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        # Colocar a la derecha de la ventana principal
        self.geometry(f"380x320+{px + pw + 10}+{py}")
        
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.resultado = None

        tk.Label(self, text=f"La IA seleccionó la casilla ({r}, {c})", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self, text=f"Motivo de la IA: {motivo}").pack()
        tk.Label(self, text=f"Valores lógicos posibles: {valores_posibles}").pack()

        frame_num = tk.Frame(self)
        frame_num.pack(pady=5)
        
        tk.Label(frame_num, text="Ingresa el número de minas vecinas:", font=("Arial", 10)).pack()
        
        estado_entry = "normal"
        if len(valores_posibles) == 1:
            tk.Label(frame_num, text="(Única opción lógica disponible, no se puede cambiar)", fg="gray", font=("Arial", 8)).pack()
            estado_entry = "readonly"

        self.var_num = tk.StringVar(value=str(valores_posibles[0]) if valores_posibles else "0")
        
        row_frame = tk.Frame(frame_num)
        row_frame.pack(pady=10)

        entr_num = tk.Entry(row_frame, textvariable=self.var_num, width=3,
                            font=("Arial", 24, "bold"), justify="center",
                            state=estado_entry, relief="solid", bd=2, readonlybackground="#f0f0f0")
        entr_num.pack(side=tk.LEFT, padx=10)
        
        btn_num = tk.Button(row_frame, text="Revelar Número", font=("Arial", 10, "bold"), bg="#a5d6a7", cursor="hand2", command=self.revelar_numero)
        btn_num.pack(side=tk.LEFT, padx=5)

        btn_mina = tk.Button(self, text="¡Es una mina! 💥", font=("Arial", 12, "bold"), bg="#ffadad", cursor="hand2", command=self.es_mina)
        btn_mina.pack(pady=10)

        if not permite_mina:
            btn_mina.config(state="disabled")
            tk.Label(self, text="(La IA dedujo que aquí es seguro. No puedes mentir.)", fg="red", font=("Arial", 8)).pack()

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def revelar_numero(self):
        try:
            val = int(self.var_num.get())
            self.resultado = {"tipo": "numero", "valor": val}
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.", parent=self)

    def es_mina(self):
        self.resultado = {"tipo": "mina"}
        self.destroy()

    def cerrar(self):
        self.resultado = None
        self.destroy()

class BuscaminasExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscaminas")
        self.filas = 10
        self.columnas = 10
        
        # Tablero de la IA (None: desconocido, 'S': seguro pendiente, 'M': mina, int: revelado)
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

    def casilla_puede_ser_segura(self, r, c):
        """
        Verifica si revelar (r, c) como casilla segura no rompe
        las restricciones de los números vecinos ya revelados.
        """
        for vr, vc in self.obtener_vecinos(r, c):
            val = self.tablero_ia[vr][vc]
            if isinstance(val, int):
                vecinos_num = self.obtener_vecinos(vr, vc)
                flags = sum(1 for x, y in vecinos_num if self.tablero_ia[x][y] == 'M')
                # Simular que (r, c) deja de estar oculta porque fue revelada
                ocultos_restantes = sum(
                    1
                    for x, y in vecinos_num
                    if self.tablero_ia[x][y] is None and (x, y) != (r, c)
                )
                # Si ya no alcanza para completar el número, esta casilla no puede ser segura.
                if flags + ocultos_restantes < val:
                    return False
        return True

    def colocacion_mina_valida(self, r, c):
        """
        Verifica si (r, c) puede marcarse como mina sin exceder
        el valor de ningun numero vecino.
        """
        for vr, vc in self.obtener_vecinos(r, c):
            val = self.tablero_ia[vr][vc]
            if isinstance(val, int):
                vecinos_num = self.obtener_vecinos(vr, vc)
                flags = sum(1 for x, y in vecinos_num if self.tablero_ia[x][y] == 'M')
                if flags + 1 > val:
                    return False
        return True

    def tablero_consistente(self):
        """
        Comprueba que para cada numero revelado se cumpla:
        banderas <= valor <= banderas + ocultas.
        """
        for r in range(self.filas):
            for c in range(self.columnas):
                val = self.tablero_ia[r][c]
                if isinstance(val, int):
                    vecinos = self.obtener_vecinos(r, c)
                    flags = sum(1 for vr, vc in vecinos if self.tablero_ia[vr][vc] == 'M')
                    ocultas = sum(1 for vr, vc in vecinos if self.tablero_ia[vr][vc] is None)
                    if flags > val:
                        return False
                    if flags + ocultas < val:
                        return False
        return True

    def valores_posibles_casilla(self, r, c):
        """
        Calcula los valores validos para (r, c) verificando
        consistencia global del tablero.
        """
        vecinos_objetivo = self.obtener_vecinos(r, c)
        flags_objetivo = sum(1 for vr, vc in vecinos_objetivo if self.tablero_ia[vr][vc] == 'M')
        vars_objetivo = {(vr, vc) for vr, vc in vecinos_objetivo if self.tablero_ia[vr][vc] is None}

        # Si no hay incógnitas alrededor, el valor queda completamente definido.
        if not vars_objetivo:
            return [flags_objetivo]

        # Construir restricciones de todos los números revelados.
        restricciones_totales = []
        for rr in range(self.filas):
            for cc in range(self.columnas):
                val = self.tablero_ia[rr][cc]
                if isinstance(val, int):
                    vnum = self.obtener_vecinos(rr, cc)
                    flags = sum(1 for vr, vc in vnum if self.tablero_ia[vr][vc] == 'M')
                    vars_num = {(vr, vc) for vr, vc in vnum if self.tablero_ia[vr][vc] is None}
                    requerido = val - flags
                    if requerido < 0 or requerido > len(vars_num):
                        return []
                    if vars_num:
                        restricciones_totales.append((vars_num, requerido))

        # Cerrar componente conectada de restricciones que afecta a la casilla objetivo.
        vars_comp = set(vars_objetivo)
        restricciones_comp = []
        cambio = True
        while cambio:
            cambio = False
            for vars_res, req in restricciones_totales:
                if vars_res & vars_comp:
                    if (vars_res, req) not in restricciones_comp:
                        restricciones_comp.append((vars_res, req))
                    nuevos = vars_res - vars_comp
                    if nuevos:
                        vars_comp.update(nuevos)
                        cambio = True

        # Si no hay restricciones conectadas, aplicar rango local simple.
        if not restricciones_comp:
            return list(range(flags_objetivo, flags_objetivo + len(vars_objetivo) + 1))

        # Limite defensivo para evitar explosión combinatoria en tableros muy abiertos.
        if len(vars_comp) > 22:
            min_local = flags_objetivo
            max_local = flags_objetivo + len(vars_objetivo)
            estado_previo = self.tablero_ia[r][c]
            posibles = []
            for num in range(min_local, max_local + 1):
                self.tablero_ia[r][c] = num
                if self.tablero_consistente():
                    posibles.append(num)
            self.tablero_ia[r][c] = estado_previo
            return posibles

        vars_lista = list(vars_comp)
        idx_var = {v: i for i, v in enumerate(vars_lista)}

        # Reindexar restricciones para backtracking rápido.
        restricciones_idx = []
        for vars_res, req in restricciones_comp:
            indices = [idx_var[v] for v in vars_res]
            restricciones_idx.append((indices, req))

        minas_objetivo_posibles = set()
        asignacion = [None] * len(vars_lista)
        idx_objetivo = {idx_var[v] for v in vars_objetivo if v in idx_var}

        def poda_valida():
            for indices, req in restricciones_idx:
                asignadas = 0
                minas_asignadas = 0
                for i in indices:
                    if asignacion[i] is not None:
                        asignadas += 1
                        minas_asignadas += asignacion[i]
                restantes = len(indices) - asignadas
                # req debe estar entre el mínimo y máximo alcanzable.
                if minas_asignadas > req:
                    return False
                if minas_asignadas + restantes < req:
                    return False
            return True

        def backtrack(pos):
            if pos == len(vars_lista):
                # Validación final estricta.
                for indices, req in restricciones_idx:
                    if sum(asignacion[i] for i in indices) != req:
                        return
                minas_en_objetivo = flags_objetivo + sum(asignacion[i] for i in idx_objetivo)
                minas_objetivo_posibles.add(minas_en_objetivo)
                return

            # Probar primero 0 para priorizar jugadas más conservadoras.
            for valor in (0, 1):
                asignacion[pos] = valor
                if poda_valida():
                    backtrack(pos + 1)
                asignacion[pos] = None

        backtrack(0)
        return sorted(minas_objetivo_posibles)

    def marcar_como_segura(self, r, c):
        if self.tablero_ia[r][c] is None:
            self.tablero_ia[r][c] = 'S'
            self.botones[r][c].config(bg="#d9fdd3")
            return True
        return False

    def restaurar_estilo_casilla(self, r, c):
        estado = self.tablero_ia[r][c]
        if estado == 'M':
            self.botones[r][c].config(text="🚩", bg="#ffadad", fg="black", relief="raised")
        elif estado == 'S':
            self.botones[r][c].config(text="", bg="#d9fdd3", fg="black", relief="raised")
        elif isinstance(estado, int):
            self.botones[r][c].config(text=str(estado), bg="#ffffff", fg="black", relief="sunken")
        else:
            self.botones[r][c].config(text="", bg="#d1d1d1", fg="black", relief="raised")

    def pedir_dato(self, r, c, motivo):
        self.botones[r][c].config(bg="#80d8ff") # Iluminar azul para seleccionada
        self.root.update()

        try:
            # Rango logico real (no solo local), validado contra todo el tablero.
            valores_posibles = self.valores_posibles_casilla(r, c)
            if not valores_posibles:
                messagebox.showerror(
                    "Contradicción",
                    f"No existe ningún valor válido para ({r}, {c}) con el estado actual.\n"
                    "Revisa números ingresados previamente."
                )
                self.restaurar_estilo_casilla(r, c)
                return

            min_val = min(valores_posibles)
            max_val = max(valores_posibles)

            permite_mina = "Segura" not in motivo

            dialogo = DialogoPC(self.root, r, c, motivo, valores_posibles, permite_mina)
            self.root.wait_window(dialogo)
            
            res = dialogo.resultado
            
            if res is None:
                self.restaurar_estilo_casilla(r, c)
                return
                
            if res["tipo"] == "mina":
                self.tablero_ia[r][c] = 'X'
                self.botones[r][c].config(text="💥", bg="#ff3333", fg="black", relief="raised")
                messagebox.showinfo("¡Has Ganado!", "¡La IA ha pisado una mina!\nComo PC, has ganado la partida.")
                return # Detiene el analisis

            num = res["valor"]

            # Validacion exacta: solo permitir valores realmente compatibles con todo el tablero.
            if num not in valores_posibles:
                messagebox.showerror(
                    "Error",
                    f"Valor incorrecto. Para esta casilla solo se permite: {valores_posibles}."
                )
                self.restaurar_estilo_casilla(r, c)
                self.root.after(300, lambda: self.pedir_dato(r, c, motivo))
                return

            # Validación lógica global: si revelar esta casilla rompe un número vecino,
            # entonces esta casilla debía ser mina.
            if not self.casilla_puede_ser_segura(r, c):
                self.tablero_ia[r][c] = 'M'
                self.botones[r][c].config(text="🚩", bg="#ffadad", fg="black")
                messagebox.showwarning(
                    "Corrección lógica",
                    f"La casilla ({r}, {c}) no puede ser segura por restricciones vecinas.\n"
                    "Se marcó automáticamente como mina."
                )
                self.analizar_tablero()
                return

            # Validacion global: el numero ingresado no debe generar contradicciones
            # con el resto del tablero revelado.
            estado_previo = self.tablero_ia[r][c]
            self.tablero_ia[r][c] = num
            if not self.tablero_consistente():
                self.tablero_ia[r][c] = estado_previo
                messagebox.showerror(
                    "Error lógico",
                    f"El valor {num} en ({r}, {c}) genera una contradicción con números vecinos.\n"
                    "Revisa el valor e inténtalo de nuevo."
                )
                self.restaurar_estilo_casilla(r, c)
                self.root.after(300, lambda: self.pedir_dato(r, c, motivo))
                return

            # Guardamos en la memoria de la IA
            self.botones[r][c].config(text=str(num), bg="#ffffff", relief="sunken", fg="black")
            self.analizar_tablero()
        except Exception as exc:
            # Evita que se cierre la app por errores inesperados de lógica.
            messagebox.showerror("Error interno", f"Ocurrió un error y el juego continúa:\n{exc}")
            self.restaurar_estilo_casilla(r, c)

    def analizar_tablero(self):
        # 1. Bucle para marcar casillas seguras y minas evidentes
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

                        # Si ya hay suficientes minas marcadas, los desconocidos vecinos son seguros.
                        if len(flags) == val and len(ocultos) > 0:
                            for vr, vc in ocultos:
                                if self.marcar_como_segura(vr, vc):
                                    hubo_cambio = True

                        # Si (ocultos + banderas) = valor de la celda, los ocultos restantes son minas.
                        if len(ocultos) + len(flags) == val and len(ocultos) > 0:
                            for vr, vc in ocultos:
                                if self.colocacion_mina_valida(vr, vc):
                                    self.tablero_ia[vr][vc] = 'M'
                                    self.botones[vr][vc].config(text="🚩", bg="#ffadad", fg="black")
                                    hubo_cambio = True

        # 2. Destapar primero las casillas ya deducidas como seguras
        for r in range(self.filas):
            for c in range(self.columnas):
                if self.tablero_ia[r][c] == 'S':
                    self.pedir_dato(r, c, "Casilla 100% Segura")
                    return

        # 3. Buscar casillas seguras adicionales por regla local
        for r in range(self.filas):
            for c in range(self.columnas):
                val = self.tablero_ia[r][c]
                if isinstance(val, int):
                    vecinos = self.obtener_vecinos(r, c)
                    flags = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] == 'M']
                    ocultos = [v for v in vecinos if self.tablero_ia[v[0]][v[1]] is None]
                    
                    # Si ya tengo todas las banderas listas para un número, los otros ocultos son seguros
                    if len(flags) == val and len(ocultos) > 0:
                        for sr, sc in ocultos:
                            if self.casilla_puede_ser_segura(sr, sc):
                                self.pedir_dato(sr, sc, "Casilla 100% Segura")
                                return

        # 4. Si no hay celdas lógicas, aplicar cálculo probabilístico básico
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
            candidatas = sorted(riesgos, key=riesgos.get)
            for mejor_casilla in candidatas:
                if self.casilla_puede_ser_segura(mejor_casilla[0], mejor_casilla[1]):
                    min_riesgo = riesgos[mejor_casilla]
                    self.pedir_dato(mejor_casilla[0], mejor_casilla[1], f"Probabilidad, Riesgo: {min_riesgo:.2f}")
                    return
            # Si ninguna candidata puede ser segura, el estado actual del tablero es contradictorio.
            messagebox.showerror("Contradicción", "No hay jugadas seguras con el estado actual. Revisa los números ingresados.")
        else:
            messagebox.showinfo("Fin del Análisis", "No quedan más casillas que analizar o el tablero está completo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuscaminasExperto(root)
    root.mainloop()