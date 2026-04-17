# IA Buscaminas: Simulador de Pensamiento Humano

Este proyecto es una herramienta interactiva desarrollada en **Python** que emula el proceso de toma de decisiones de un experto en Buscaminas. A diferencia de un juego tradicional, este programa actúa como un **agente inteligente** que utiliza lógica deductiva y análisis probabilístico para resolver el tablero.

La IA no tiene acceso a la solución; requiere que el usuario actúe como el "entorno", proporcionando los datos de las casillas que la IA decide explorar.

## Características Principales

* **Deducción Lógica (Certezas):** El algoritmo identifica minas garantizadas basándose en el conteo de vecinos y banderas colocadas.
* **Análisis Probabilístico:** Cuando no existe un movimiento 100% seguro, la IA calcula el riesgo de cada casilla disponible y selecciona la de menor probabilidad de error.
* **Gestión de Expansión:** Implementa lógica de propagación automática cuando se detectan casillas con valor "0".
* **Interfaz Gráfica:** Construida con `Tkinter`, ofreciendo una visualización clara del estado del tablero (oculto, numerado o mina deducida).

## Lógica de Resolución

El agente sigue un flujo jerárquico de pensamiento:

1.  **Primer Movimiento:** Selección aleatoria para iniciar la recolección de datos.
2.  **Capa de Certeza:** * Si $CasillasOcultas + Banderas = NumeroCasilla$, entonces todas las ocultas son minas.
    * Si $Banderas = NumeroCasilla$, todas las demás ocultas son seguras.
3.  **Capa de Riesgo:** Si la lógica anterior no arroja resultados, se aplica un cálculo de riesgo relativo sumando las probabilidades locales de cada vecino numérico para elegir el camino menos peligroso.

## Instalación y Uso

### Requisitos
* Python 3.x
* Tkinter

### Ejecución
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/nombre-de-tu-repo.git](https://github.com/tu-usuario/nombre-de-tu-repo.git)
