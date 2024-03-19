import pygame
import random

# Définition des variables globales
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 5

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Définition de la classe Snake
class Snake:
    def __init__(self, head_image, body_image, tail_image):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.head_image = head_image
        self.body_image = body_image
        self.tail_image = tail_image
        self.body_segments = []

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.body_segments = []

    def draw(self, surface):
        # Dessiner la queue
        if len(self.positions) > 1:
            tail_pos = self.positions[-1]
            surface.blit(self.tail_image, tail_pos)

        # Dessiner la tête
        head_pos = self.positions[0]
        surface.blit(self.head_image, head_pos)

        # Dessiner le corps
        for segment in self.body_segments:
            surface.blit(self.body_image, segment)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Définition de la classe Food
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)

# Définition des directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    # Charger les images pour la tête, le corps et la queue du serpent
    head_image = pygame.image.load('head.png').convert_alpha()
    body_image = pygame.image.load('body.png').convert_alpha()
    tail_image = pygame.image.load('tail.png').convert_alpha()

    # Redimensionner les images pour correspondre à la taille de la grille
    head_image = pygame.transform.scale(head_image, (GRID_SIZE, GRID_SIZE))
    body_image = pygame.transform.scale(body_image, (GRID_SIZE, GRID_SIZE))
    tail_image = pygame.transform.scale(tail_image, (GRID_SIZE, GRID_SIZE))

    snake = Snake(head_image, body_image, tail_image)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        snake.handle_keys()
        snake.move()

        # Collision avec la nourriture
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()
            # Ajouter un segment de corps
            if len(snake.body_segments) == 0:
                snake.body_segments.append(snake.positions[-1])
            else:
                snake.body_segments.append(snake.body_segments[-1])

        # Dessiner l'écran de jeu
        surface.fill(WHITE)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(INITIAL_SPEED + snake.length // 3)

if __name__ == "__main__":
    main()
