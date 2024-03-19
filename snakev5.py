import pygame
import random
import sys

# Définition des variables globales
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 5

# Couleurs
WHITE = (255, 255, 255)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)

# Définition de la classe Snake
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = PURPLE
        self.game_started = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
            self.game_started = True  # Marquer que le jeu a commencé

    def move(self):
        if not self.game_started:
            return  # Ne rien faire si le jeu n'a pas encore commencé

        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))
        if new in self.positions or new[0] < 0 or new[0] >= SCREEN_WIDTH or new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            # Si le serpent touche les bords ou lui-même, recommencer le jeu
            self.reset()
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    # Dans la classe Snake
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.game_started = False  # Remettre à False lorsque le jeu est réinitialisé
        return True  # Retourner True pour indiquer que le jeu a été réinitialisé

    # Dans la boucle principale

    # Déplacement du serpent
    if snake.move():
        # Collision avec la nourriture
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            if score > best_score:
                best_score = score
                save_best_score(best_score)  # Enregistrer le nouveau meilleur score
            food.randomize_position()
    else:
        if not snake.reset():
            score = 0  # Réinitialiser le score uniquement si le jeu n'a pas été réinitialisé

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.turn(UP)
        elif keys[pygame.K_DOWN]:
            self.turn(DOWN)
        elif keys[pygame.K_LEFT]:
            self.turn(LEFT)
        elif keys[pygame.K_RIGHT]:
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
        pygame.draw.rect(surface, WHITE, r, 1)

# Définition des directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    snake = Snake()
    food = Food()
    score = 0
    best_score = load_best_score()  # Charger le meilleur score
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Gestion des touches
        snake.handle_keys()
        
        # Déplacement du serpent
        if snake.move():
            # Collision avec la nourriture
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)  # Enregistrer le nouveau meilleur score
                food.randomize_position()
        
        # Dessiner l'écran de jeu
        surface.fill(WHITE)
        draw_grid(surface)  # Dessiner le cadrillage
        snake.draw(surface)
        food.draw(surface)
        
        # Afficher le score et le meilleur score
        draw_score(surface, score, best_score)
        
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(INITIAL_SPEED + snake.length // 3)

def draw_score(surface, score, best_score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    best_score_text = font.render(f"Best: {best_score}", True, (0, 0, 0))
    surface.blit(score_text, (10, 10))
    surface.blit(best_score_text, (10, 50))

def load_best_score():
    try:
        with open("best_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_best_score(best_score):
    with open("best_score.txt", "w") as file:
        file.write(str(best_score))

if __name__ == "__main__":
    main()
