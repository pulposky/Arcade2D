"# 🎰 Blackjack - Casino 21

Juego de Blackjack clásico desarrollado en Python usando Pygame. Experimenta la emoción del casino con gráficos generados por código y un sistema completo de apuestas.

## ✨ Características

- 🎴 **Gráficos generados por código** - Cartas dibujadas dinámicamente sin necesidad de imágenes externas
- 💰 **Sistema de apuestas** - Comienza con $1000 en fichas y gestiona tu bankroll
- 🎨 **Estilo casino clásico** - Mesa verde, cartas tradicionales y colores dorados
- 🤖 **IA del Dealer** - El croupier sigue las reglas tradicionales (pide hasta 17)
- ⚡ **Controles intuitivos** - Juega con mouse o teclado
- 🎯 **Reglas estándar** - Blackjack natural paga 2.5x, reglas básicas de 21

## 📋 Requisitos

- Python 3.7 o superior
- Pygame 2.5.2

## 🚀 Instalación

1. Clona o descarga el repositorio:
```bash
git clone <tu-repositorio>
cd blackjack-game
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el juego:
```bash
python main.py
```

## 🎮 Cómo Jugar

### Inicio del Juego
1. Al iniciar, tendrás $1000 en fichas
2. Selecciona tu apuesta usando los botones rápidos o ingresa un monto personalizado
3. Presiona \"APOSTAR\" o ENTER para comenzar la ronda

### Durante la Partida
- Recibirás 2 cartas visibles
- El dealer recibirá 2 cartas (una oculta)
- **Objetivo:** Acercarte a 21 sin pasarte
- Decide si pedir más cartas o plantarte
- El dealer revelará su carta y jugará automáticamente

### Controles

#### Pantalla de Apuestas
- **Click** en los botones de monto rápido ($10, $25, $50, $100, $250, $500)
- **Teclado numérico** + **ENTER** para apuesta personalizada
- **BACKSPACE** para borrar

#### Durante el Juego
- **H** o **ESPACIO**: Pedir carta (Hit)
- **S** o **ENTER**: Plantarse (Stand)
- **Click** en los botones de la pantalla

## 📜 Reglas del Juego

### Valores de las Cartas
- **Números 2-10**: Valor nominal
- **J, Q, K**: Valen 10 puntos
- **As**: Vale 11 u 1 (se ajusta automáticamente)

### Reglas Básicas
1. **Objetivo**: Sumar 21 o acercarse sin pasarse
2. **Blackjack Natural**: As + carta de 10 en las primeras 2 cartas (paga 2.5x)
3. **Bust**: Si superas 21, pierdes automáticamente
4. **Dealer**: Debe pedir hasta tener 17 o más
5. **Empate (Push)**: Si empatas con el dealer, recuperas tu apuesta

### Apuestas
- **Mínima**: $10
- **Máxima**: $500
- **Apuesta ganadora**: 2x tu apuesta (2.5x con Blackjack natural)
- Si pierdes todas tus fichas, se reinician a $1000

## 📁 Estructura del Proyecto

```
/app/
├── main.py                 # Punto de entrada del juego
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
└── src/                   # Código fuente
    ├── __init__.py       # Inicialización del paquete
    ├── constants.py      # Constantes (colores, dimensiones, config)
    ├── card.py           # Clases Card y Deck
    ├── player.py         # Clases Player y Dealer
    ├── game.py           # Lógica principal del juego
    └── ui.py             # Interfaz gráfica con Pygame
```

## 🎯 Capturas del Juego

### Pantalla de Apuestas
- Muestra tu balance de fichas
- Botones de apuesta rápida
- Campo de entrada para montos personalizados

### Pantalla de Juego
- Cartas del dealer (una oculta hasta que te plantes)
- Tus cartas visibles
- Panel de información con apuesta actual y fichas restantes
- Botones de acción (PEDIR / PLANTARSE)
- Mensajes de estado del juego

## 🛠️ Desarrollo

### Módulos Principales

**constants.py**
- Configuración de colores, dimensiones y parámetros del juego
- Fuentes y estilos visuales

**card.py**
- `Card`: Representa una carta individual con palo y rango
- `Deck`: Baraja de 52 cartas con funcionalidad de mezcla

**player.py**
- `Player`: Gestiona la mano, fichas y apuestas del jugador
- `Dealer`: Implementa la lógica automática del croupier

**game.py**
- `BlackjackGame`: Controla el flujo del juego y las reglas
- Gestiona estados (apostando, jugando, turno dealer, fin)

**ui.py**
- `BlackjackUI`: Renderiza la interfaz gráfica
- Maneja eventos de usuario y actualiza la pantalla

## 🎨 Personalización

Puedes modificar fácilmente el juego editando `src/constants.py`:

```python
# Cambiar colores
CASINO_GREEN = (53, 101, 77)  # Color de la mesa
GOLD = (255, 215, 0)          # Color de acentos

# Ajustar configuración
INITIAL_CHIPS = 1000          # Fichas iniciales
MIN_BET = 10                  # Apuesta mínima
MAX_BET = 500                 # Apuesta máxima

# Dimensiones de ventana
WIDTH = 1000
HEIGHT = 700
```

## 🐛 Solución de Problemas

**El juego no inicia:**
- Verifica que Pygame esté instalado: `pip install pygame`
- Comprueba la versión de Python: `python --version` (debe ser 3.7+)

**Las cartas no se muestran correctamente:**
- Asegúrate de que todas las fuentes del sistema estén disponibles
- Pygame inicializa fuentes automáticamente

**Error de importación:**
- Ejecuta desde el directorio raíz: `/app/`
- Verifica que la carpeta `src/` exista con todos los archivos

## 🎓 Posibles Mejoras Futuras

- [ ] Agregar sonidos (barajar, repartir, ganar/perder)
- [ ] Implementar reglas avanzadas (dividir, doblar, seguro)
- [ ] Modo multijugador local
- [ ] Sistema de estadísticas y récords
- [ ] Animaciones de cartas
- [ ] Diferentes temas visuales
- [ ] Guardar progreso del jugador

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como proyecto educativo de Python y Pygame.

## 🙏 Agradecimientos

- Pygame community por la excelente documentación
- Reglas de Blackjack basadas en estándares de casinos

---

**¡Diviértete jugando y que la suerte esté de tu lado! 🍀♠️♥️♦️♣️**
"