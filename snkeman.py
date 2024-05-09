import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# Taille de l'écran
dis_size = 600

# Création de la fenêtre de jeu
dis = pygame.display.set_mode((dis_size, dis_size))

# Titre de la fenêtre
pygame.display.set_caption('Jeu de Serpent')

# Définition des couleurs
white = (255, 255, 255)
red = (213, 50, 80)
dark_green = (92, 123, 53)
light_green = (138, 156, 78)
blue = (50, 153, 213)

# Taille d'un bloc du serpent et sa vitesse
snake_block = 20
snake_speed = 15

# Horloge pour gérer le temps du jeu
clock = pygame.time.Clock()

# Initialisation des sons
pygame.mixer.init()
son_manger = pygame.mixer.Sound('sound/eat.wav')
son_manger.set_volume(0.2)  # Réduit le volume à 90% de l'original
son_collision = pygame.mixer.Sound('sound/collision.wav')

# Chargement des images
head_img = pygame.image.load('Images/assets/head.png').convert_alpha()
body_img = pygame.image.load('Images/assets/body.png').convert_alpha()
tail_img = pygame.image.load('Images/assets/tail.png').convert_alpha()
apple_img = pygame.image.load('Images/assets/letchi_snake_game.png').convert_alpha()

# Redimensionnement des images pour qu'elles correspondent à la taille du bloc du serpent
head_img = pygame.transform.scale(head_img, (snake_block, snake_block))
body_img = pygame.transform.scale(body_img, (snake_block, snake_block))
tail_img = pygame.transform.scale(tail_img, (snake_block, snake_block))
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

# Définition des polices de texte
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Meilleur score initialisé à 0
best_score = 0

# Fonction pour dessiner un bouton
def draw_button(text, center_x, center_y):
    font = pygame.font.SysFont("bahnschrift", 35)
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(center=(center_x, center_y))
    pygame.draw.rect(dis, blue, text_rect.inflate(20, 10), border_radius=5)
    dis.blit(text_render, text_rect)
    return text_rect

# Fonction du menu principal
def menu_principal():
    while True:
        dis.fill(dark_green)
        start_btn = draw_button("Commencer", dis_size // 2, dis_size // 2 - 40)
        quit_btn = draw_button("Quitter", dis_size // 2, dis_size // 2 + 40)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.collidepoint(event.pos):
                    gameLoop()
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Fonction pour afficher le score actuel
def your_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, (0, 0))

# Fonction pour afficher le meilleur score
def best_score_display(score):
    value = score_font.render(f"Best Score: {score}", True, white)
    dis.blit(value, (0, 30))

# Fonction pour afficher un message
def message(msg, color):
    lines = msg.split('\n')
    y_offset = 0
    for line in lines:
        mesg = font_style.render(line, True, color)
        mesg_rect = mesg.get_rect(center=(dis_size / 2, dis_size / 2 + y_offset))
        dis.blit(mesg, mesg_rect)
        y_offset += font_style.get_linesize()

# Fonction pour dessiner l'arrière-plan
def draw_background():
    """Dessine un damier en arrière-plan."""
    for row in range(0, dis_size, snake_block):
        for col in range(row % (snake_block * 2), dis_size, snake_block * 2):
            pygame.draw.rect(dis, light_green if (row / snake_block) % 2 == 0 else dark_green, [col, row, snake_block, snake_block])

# Fonction pour dessiner le serpent
def draw_snake(snake_list):
    for i, seg in enumerate(snake_list):
        x, y, dir = seg
        img = head_img if i == len(snake_list) - 1 else body_img
        img_rotated = pygame.transform.rotate(img, dir)
        dis.blit(img_rotated, (x, y))

# Fonction principale du jeu
def gameLoop():
    global best_score
    game_over = False
    game_close = False

    x1 = dis_size / 2
    y1 = dis_size / 2
    x1_change = 0
    y1_change = 0
    direction = 0

    snake_List = [[x1, y1, direction]]
    Length_of_snake = 1

    # Position aléatoire de la pomme
    foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            dis.fill(red)
            message("Tu as perdu ! Appuie sur 'C' pour rejouer ou 'Q' pour quitter", white)
            your_score(Length_of_snake - 1)
            best_score_display(best_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = -180
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 90
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    direction = -90

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_size or x1 < 0 or y1 >= dis_size or y1 < 0:
            son_collision.play()
            game_close = True

        # Afficher le damier de couleur
        for row in range(0, dis_size, snake_block * 2):
            for col in range(0, dis_size, snake_block * 2):
                pygame.draw.rect(dis, light_green, [col, row, snake_block, snake_block])
                pygame.draw.rect(dis, dark_green, [col + snake_block, row, snake_block, snake_block])
                pygame.draw.rect(dis, dark_green, [col, row + snake_block, snake_block, snake_block])
                pygame.draw.rect(dis, light_green, [col + snake_block, row + snake_block, snake_block, snake_block])
        
        dis.blit(apple_img, (foodx, foody))

        snake_Head = [x1, y1, direction]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_List)
        your_score(Length_of_snake - 1)
        best_score_display(best_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            if (Length_of_snake - 1) > best_score:
                best_score = Length_of_snake - 1
            son_manger.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Lancement du menu principal
menu_principal()
