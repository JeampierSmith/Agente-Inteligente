import pygame
import random

# Configuración inicial
GRID_SIZE = 7  # Tamaño del entorno
CELL_SIZE = 80  # Tamaño de cada celda en píxeles
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # Tamaño de la ventana
FPS = 5  # Velocidad de actualización

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GREEN = (0, 200, 0)

class Environment:
    def __init__(self, size, obstacles, goal):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.agent_position = [0, 0]

        # Colocar obstáculos
        for _ in range(obstacles):
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if [x, y] != [0, 0] and [x, y] != goal:
                self.grid[x][y] = 'X'

        # Colocar el objetivo
        self.grid[goal[0]][goal[1]] = 'G'
        self.goal_position = goal

    def is_valid_move(self, position):
        x, y = position
        if 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] != 'X':
            return True
        return False

    def move_agent(self, new_position):
        if self.is_valid_move(new_position):
            self.agent_position = new_position
            return True
        return False

    def is_goal_reached(self):
        return self.agent_position == self.goal_position


class Agent:
    def __init__(self, environment):
        self.env = environment
        self.visited = set()
        self.path = []

    def move(self):
        if self.env.is_goal_reached():  # Detenerse si ya se alcanzó el objetivo
            return True

        x, y = self.env.agent_position
        self.visited.add((x, y))

        # Definir posibles movimientos: arriba, abajo, izquierda, derecha
        moves = [
            (x-1, y),  # arriba
            (x+1, y),  # abajo
            (x, y-1),  # izquierda
            (x, y+1)   # derecha
        ]

        # Intentar moverse a una celda válida y no visitada
        for move in moves:
            if move not in self.visited and self.env.is_valid_move(move):
                self.path.append(move)
                if self.env.move_agent(move):
                    return False  # El movimiento fue realizado, continuar

        # Si no hay movimientos válidos, retroceder
        if self.path:
            self.env.move_agent(self.path.pop())

        return False  # El agente sigue moviéndose


def draw_environment(screen, environment):
    screen.fill(WHITE)

    for x in range(environment.size):
        for y in range(environment.size):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if environment.grid[x][y] == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif environment.grid[x][y] == 'G':
                pygame.draw.rect(screen, GREEN, rect)
                # Dibujar un círculo para destacar el objetivo
                center = (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2)
                radius = CELL_SIZE // 4
                pygame.draw.circle(screen, DARK_GREEN, center, radius)
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
env = Environment(GRID_SIZE, obstacles=10, goal=[6, 6])
agent = Agent(env)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover al agente solo si no ha alcanzado el objetivo
    if not env.is_goal_reached():
        if agent.move():  # El agente se detiene si llega al objetivo
            print("¡El agente alcanzó el objetivo!")
            running = False
    else:
        print("¡El agente alcanzó el objetivo!")
        running = False  # Salir del bucle si alcanza el objetivo

    # Dibujar entorno
    draw_environment(screen, env)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
