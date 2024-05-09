import pygame
import random

pygame.init()

# Définition des couleurs
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (92, 123, 53)
light_green = (138, 156, 78)

# Dimensions de l'écran de jeu
dis_size = 600
dis = pygame.display.set_mode((dis_size, dis_size))
snake_block = 20
snake_speed = 15

# Horloge pour contrôler les FPS
clock = pygame.time.Clock()

# Chargement des images
head_img = pygame.transform.scale(pygame.image.load('Images/assets/head.png'), (snake_block, snake_block))
body_img = pygame.transform.scale(pygame.image.load('Images/assets/body.png'), (snake_block, snake_block))
tail_img = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/assets/tail.png'), (snake_block, snake_block)), True, False)
apple_img = pygame.transform.scale(pygame.image.load('Images/assets/letchi_snake_game.png'), (snake_block, snake_block))

# Police pour les scores et les messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Variable pour enregistrer le meilleur score
best_score = 0

# Fonction pour afficher le score
def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

# Fonction pour afficher le meilleur score
def best_score_display(score):
    value = score_font.render("Best Score: " + str(score), True, white)
    dis.blit(value, [0, 30])

# Fonction pour dessiner le serpent
def draw_snake(snake_list, direction):
    for i, segment in enumerate(snake_list):
        if i == 0:  # Tête
            img = pygame.transform.rotate(tail_img, direction)
        elif i == len(snake_list) - 1:  # Queue
            img = pygame.transform.rotate(head_img, direction)
        else:  # Corps
            img = body_img
            # Rotation du corps pour qu'il s'aligne avec la direction de la tête
            if direction == 0:
                img = pygame.transform.rotate(body_img, 0)
            elif direction == 90:
                img = pygame.transform.rotate(body_img, 90)
            elif direction == 180:
                img = pygame.transform.rotate(body_img, 180)
            elif direction == -90:
                img = pygame.transform.rotate(body_img, -90)
        dis.blit(img, segment)

# Fonction pour afficher un message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_size / 6, dis_size / 3])

# Fonction principale du jeu
def gameLoop():
    global best_score

    game_over = False
    game_close = False

    # Position initiale du serpent
    x1 = dis_size / 2
    y1 = dis_size / 2
    x1_change = 0
    y1_change = 0

    snake_List = [[x1, y1]]
    Length_of_snake = 1

    # Génération aléatoire de la position de la pomme
    foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block

    direction = 0  # Direction de la tête du serpent (angle de rotation)

    while not game_over:

        while game_close:
            dis.fill(red)
            message("Tu as perdu ! Appuie sur 'C' pour rejouer ou 'Q' pour quitter", white)
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
                    direction = 180  # Rotation de la tête vers la gauche
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 0  # Rotation de la tête vers la droite
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 90  # Rotation de la tête vers le haut
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    direction = -90  # Rotation de la tête vers le bas

        if x1 >= dis_size or x1 < 0 or y1 >= dis_size or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Afficher le damier de couleur
        for row in range(0, dis_size, snake_block * 2):
            for col in range(0, dis_size, snake_block * 2):
                pygame.draw.rect(dis, light_green, [col, row, snake_block, snake_block])
                pygame.draw.rect(dis, dark_green, [col + snake_block, row, snake_block, snake_block])
                pygame.draw.rect(dis, dark_green, [col, row + snake_block, snake_block, snake_block])
                pygame.draw.rect(dis, light_green, [col + snake_block, row + snake_block, snake_block, snake_block])

        dis.blit(apple_img, (foodx, foody))  # Afficher l'image de la pomme

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        draw_snake(snake_List, direction)
        your_score(Length_of_snake - 1)
        best_score_display(best_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            if (Length_of_snake - 1)> best_score:
                best_score = Length_of_snake - 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

