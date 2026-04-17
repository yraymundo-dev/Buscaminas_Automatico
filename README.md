# Inteligencia Artificial - Buscaminas (Simulador Experto)

Este proyecto es una aplicación desarrollada en **Python** que emula el proceso de toma de decisiones de un motor de Inteligencia Artificial enfocado en el clásico juego **Buscaminas**. Fue diseñado como un proyecto práctico de algoritmos de inteligencia artificial, manteniendo el código limpio, intuitivo y con un enfoque de "agente deductivo-matemático".

A diferencia de un jugador o bot clásico que tiene acceso directo a la memoria del juego, **este programa actúa como un simulador interactivo de pensamiento**: la IA calcula los movimientos, y tú (el usuario) actúas como sus "ojos" suministrándole la cantidad de minas de las casillas que ella te va pidiendo. 

## Características Clave del Algoritmo

Este proyecto implementa **técnicas de inteligencia artificial simbólica** combinadas con **análisis de probabilidades** para guiar al usuario hacia la victoria.

*   **Deducción Lógica (Certeza al 100%):** Utiliza reglas proposicionales locales. Si las banderas coinciden con el número central, el resto es seguro. Si el total de casillas ocultas más las banderas es igual al número central, todas las casillas ocultas son minas garantizadas. Las casillas 100% lógicas se escogen primero sin fallas.
*   **Análisis Probabilístico:** Frente a escenarios sin salidas lógicas (certezas), la IA evalúa el área local de las casillas ocultas utilizando las probabilidades impuestas por las casillas reveladas alrededor. Luego, arroja el movimiento estadísticamente más seguro mostrando su puntaje de "riesgo".
*   **Asistente Anti-Errores (Validación de Rango Guiada):** El sistema fue mejorado para evitar bloqueos por estados imposibles al teclear. Al seleccionar una casilla, la IA lee su conocimiento global alrededor y le aconseja e impide al usuario ingresar un dato que viole las leyes del tablero. Te exigirá un número que encaje lógicamente entre los "mínimos" y "máximos" tolerables.
*   **Expansión Cero:** Soporte nativo para simular el barrido de zonas vacías (0s) al igual que el juego original, acelerando las decisiones.

## Lógica Interna del Motor (Cómo decide la IA)

El agente opera ejecutando constantemente un bucle de tres directivas:

1.  **Deducción de Banderas Explicitas:**  Limpia e iterativamente marca todas las casillas de su memoria que, combinando los números y posiciones actuales, correspondan matemáticamente a una mina indiscutible.
2.  **Destape de Casillas Seguras:** Busca cualquier celda numérica cuyas minas ya fueron completamente marcadas a su alrededor, apuntando la primera celda vecina oculta con un estatus de "100% Segura".
3.  **Cálculo Numérico de Probabilidad:**  Al carecer de certezas lógicas previas, itera cada casilla libre y deduce el cociente entre minas faltantes y espacios no revelados, apilando el riesgo. Decide por la casilla flotante de menor cociente de peligro.

## Ejecución del Sistema

No se requiere de bibliotecas externas pesadas. Su entorno visual ligero utiliza las ventanas y librerías nativas de tu sistema.

### Requisitos:
* Python 3.10 o superior.
* `tkinter` (ya viene pre-empaquetado de manera nativa en Windows y macOS en instalaciones comunes de Python).

### Pasos de Ejecución:
1. Clona el repositorio desde la consola de comandos.
   ```bash
   git clone https://github.com/yraymundo-dev/Buscaminas_Automatico.git
   ```
2. Accede al territorio del proyecto.
   ```bash
   cd Buscaminas_Automatico
   ```
3. Ejecuta el archivo principal.
   ```bash
   python BuscaMinas.py
   ```

Simplemente sigue el cuadro de diálogo flotante donde la IA te dictará qué casilla analizar y tú introducirás el contexto visual real. ¡Diviértete enseñándole a la IA a resolver los tableros más complejos!
