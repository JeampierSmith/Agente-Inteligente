import pygame
import random

# Configuración inicial
<<<<<<< HEAD
WINDOW_SIZE = 600  # Tamaño fijo de la ventana
FPS = 5  # Velocidad de actualización
=======
GRID_SIZE = 7  # Tamaño del entorno
CELL_SIZE = 80  # Tamaño de cada celda en píxeles
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # Tamaño de la ventana
FPS = 2  # Velocidad de actualización
>>>>>>> 081c2cc7f3dcc623a729129f131b87f7a3f96be2

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

class Environment:
    def __init__(self, size, obstacles):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.agent_position = [0, 0]

        # Colocar obstáculos
        for _ in range(obstacles):
            while True:
                x, y = random.randint(0, size-1), random.randint(0, size-1)
                if [x, y] != [0, 0] and self.grid[x][y] != 'X':
                    self.grid[x][y] = 'X'
                    break

    def is_valid_move(self, position):
        x, y = position
        if 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] != 'X':
            return True
        return False

    def move_agent(self, new_position):
        if self.is_valid_move(new_position):
            self.agent_position = new_position
            self.grid[new_position[0]][new_position[1]] = 'O'  # Marcar como visitado
            return True
        return False

class Agent:
    def __init__(self, environment):
        self.env = environment
        self.visited = set()  # Para rastrear las celdas visitadas
        self.stack = []  # Pila para manejar los movimientos del DFS

    def explore(self):
        # Obtener la posición actual del agente
        x, y = self.env.agent_position
        self.visited.add((x, y))  # Marcar como visitado

        # Agregar posición actual al stack si no está ya en el tope
        if not self.stack or self.stack[-1] != (x, y):
            self.stack.append((x, y))

        # Generar movimientos posibles: arriba, abajo, izquierda, derecha
        moves = [
            (x-1, y),  # arriba
            (x+1, y),  # abajo
            (x, y-1),  # izquierda
            (x, y+1)   # derecha
        ]

<<<<<<< HEAD
        # Intentar moverse a una celda válida y no visitada
=======
        # Explorar movimientos válidos
>>>>>>> 081c2cc7f3dcc623a729129f131b87f7a3f96be2
        for move in moves:
            if move not in self.visited and self.env.is_valid_move(move):
                self.env.move_agent(move)  # Mover al agente
                return False  # Continuar explorando

        # Si no hay movimientos válidos, retroceder
        if self.stack:
            self.stack.pop()  # Elimina la posición actual de la pila
            if self.stack:  # Si quedan más posiciones en el stack, retrocede
                self.env.move_agent(self.stack[-1])
                return False

        # Si el stack está vacío, la exploración termina
        print("completado. No quedan movimientos.")
        return True

<<<<<<< HEAD
def draw_environment(screen, environment, cell_size):
=======

def draw_environment(screen, environment):
>>>>>>> 081c2cc7f3dcc623a729129f131b87f7a3f96be2
    screen.fill(WHITE)

    for x in range(environment.size):
        for y in range(environment.size):
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            if environment.grid[x][y] == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif environment.grid[x][y] == 'O':
                pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Dibujar al agente
    agent_x, agent_y = environment.agent_position
    agent_rect = pygame.Rect(agent_y * cell_size, agent_x * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, BLUE, agent_rect)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Configuración del Entorno")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    size_input = ""  # Entrada inicial para el tamaño del entorno
    obstacle_input = ""  # Entrada inicial para la cantidad de obstáculos
    input_active = "size"  # Campo activo (size u obstacles)
    error_message = ""

    while True:
        screen.fill(WHITE)

        # Dibujar títulos y campos de entrada
        title_text = font.render("Configuración del Entorno", True, BLACK)
        size_label = font.render("Tamaño del entorno (n x n):", True, BLACK)
        obstacle_label = font.render("Cantidad de obstáculos:", True, BLACK)
        size_value = font.render(size_input, True, BLUE if input_active == "size" else BLACK)
        obstacle_value = font.render(obstacle_input, True, BLUE if input_active == "obstacles" else BLACK)
        instruction_text = font.render("Presiona ENTER para continuar", True, GRAY)
        error_text = font.render(error_message, True, (255, 0, 0))

        # Posicionar los textos
        screen.blit(title_text, (WINDOW_SIZE // 4, 50))
        screen.blit(size_label, (50, 150))
        screen.blit(size_value, (400, 150))
        screen.blit(obstacle_label, (50, 250))
        screen.blit(obstacle_value, (400, 250))
        screen.blit(instruction_text, (50, 350))
        if error_message:
            screen.blit(error_text, (50, 400))

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Cambiar entre los campos activos al hacer clic
                if 150 <= event.pos[1] <= 200:  # Primer campo
                    input_active = "size"
                elif 250 <= event.pos[1] <= 300:  # Segundo campo
                    input_active = "obstacles"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirmar configuración
                    if size_input.isdigit() and obstacle_input.isdigit():
                        size = int(size_input)
                        obstacles = int(obstacle_input)
                        if obstacles >= size * size:
                            error_message = "Los obstáculos deben ser menores al tamaño total del entorno."
                        else:
                            return size, obstacles
                    else:
                        error_message = "Por favor, ingresa valores numéricos válidos."
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "size" and len(size_input) > 0:
                        size_input = size_input[:-1]
                    elif input_active == "obstacles" and len(obstacle_input) > 0:
                        obstacle_input = obstacle_input[:-1]
                elif event.unicode.isdigit():  # Solo permitir dígitos
                    if input_active == "size" and len(size_input) < 2:
                        size_input += event.unicode
                    elif input_active == "obstacles" and len(obstacle_input) < 3:
                        obstacle_input += event.unicode

        pygame.display.flip()
        clock.tick(FPS)

# Bucle principal
pygame.init()
clock = pygame.time.Clock()

# Pantalla de configuración
GRID_SIZE, obstacles = main_menu()

# Ajustar el tamaño de celda dinámicamente
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Crear entorno y agente
env = Environment(GRID_SIZE, obstacles)
agent = Agent(env)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Agente Explorador")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Explorar el entorno
    if agent.explore():
        print("Exploración completada o agente bloqueado.")
        running = False

    # Imprimir la matriz en consola
    for row in env.grid:
        print(' '.join(row))
    print("\n")

    # Dibujar entorno
    draw_environment(screen, env, CELL_SIZE)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()