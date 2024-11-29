import pygame
import random

# Configuración inicial
GRID_SIZE = 7  # Tamaño del entorno
CELL_SIZE = 80  # Tamaño de cada celda en píxeles
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # Tamaño de la ventana
FPS = 2  # Velocidad de actualización

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
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if [x, y] != [0, 0]:  # Evitar colocar obstáculos en la posición inicial
                self.grid[x][y] = 'X'

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

        # Explorar movimientos válidos
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


def draw_environment(screen, environment):
    screen.fill(WHITE)

    for x in range(environment.size):
        for y in range(environment.size):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if environment.grid[x][y] == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif environment.grid[x][y] == 'O':
                pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Dibujar al agente
    agent_x, agent_y = environment.agent_position
    agent_rect = pygame.Rect(agent_y * CELL_SIZE, agent_x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, agent_rect)

# Configuración inicial
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Agente Explorador")
clock = pygame.time.Clock()

# Crear entorno y agente
env = Environment(GRID_SIZE, obstacles=20)
agent = Agent(env)

# Bucle principal
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
    draw_environment(screen, env)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
