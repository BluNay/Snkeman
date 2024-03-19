import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
purple = (183, 104, 232)

# Dimensions de l'écran de jeu
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))

# Horloge pour contrôler les FPS
clock = pygame.time.Clock()

# Définitions des blocs du serpent et de la vitesse du jeu
snake_block = 10
snake_speed = 15

# Police pour les scores et les messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Variable pour enregistrer le meilleur score
best_score = 0

def your_score(score):
    """Affiche le score actuel."""
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def best_score_display(score):
    """Affiche le meilleur score."""
    value = score_font.render("Best Score: " + str(score), True, white)
    dis.blit(value, [0, 30])

def our_snake(snake_block, snake_list):
    """Dessine le serpent."""
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """Affiche un message à l'écran."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    """Boucle principale du jeu."""
    global best_score

    game_over = False
    game_close = False

    # Position initiale du serpent
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Position initiale de la pomme
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(purple)
            message("Tu as perdu ! Appuie sur 'C' pour rejouer ou 'Q' pour quitter", red)
            your_score(Length_of_snake - 1)
            best_score_display(best_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(purple)
        pygame.draw.rect(dis, black, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        best_score_display(best_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            if (Length_of_snake - 1) > best_score:
                best_score = Length_of_snake - 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

