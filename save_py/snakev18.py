import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
dis_size = 600
dis = pygame.display.set_mode((dis_size, dis_size))
pygame.display.set_caption('Jeu de Serpent')

# Couleurs
white = (255, 255, 255)
red = (213, 50, 80)
dark_green = (92, 123, 53)
light_green = (138, 156, 78)
blue = (50, 153, 213)

# Paramètres du serpent
snake_block = 20
snake_speed = 15

# Horloge pour contrôler les FPS
clock = pygame.time.Clock()

# Sons
pygame.mixer.init()
son_manger = pygame.mixer.Sound('sound/eat.wav')
son_collision = pygame.mixer.Sound('sound/collision.wav')

# Images
head_img = pygame.image.load('Images/assets/head.png').convert_alpha()
body_img = pygame.image.load('Images/assets/body.png').convert_alpha()
tail_img = pygame.image.load('Images/assets/tail.png').convert_alpha()
apple_img = pygame.image.load('Images/assets/letchi_snake_game.png').convert_alpha()

# Redimensionnement des images
head_img = pygame.transform.scale(head_img, (snake_block, snake_block))
body_img = pygame.transform.scale(body_img, (snake_block, snake_block))
tail_img = pygame.transform.scale(tail_img, (snake_block, snake_block))
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

# Polices de texte
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Score
best_score = 0

def draw_button(text, center_x, center_y):
    font = pygame.font.SysFont("bahnschrift", 35)
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(center=(center_x, center_y))
    pygame.draw.rect(dis, blue, text_rect.inflate(20, 10), border_radius=5)
    dis.blit(text_render, text_rect)
    return text_rect

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

def your_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, (0, 0))

def best_score_display(score):
    value = score_font.render(f"Best Score: {score}", True, white)
    dis.blit(value, (0, 30))

def draw_snake(snake_list):
    for i, seg in enumerate(snake_list):
        x, y, dir = seg
        img = head_img if i == len(snake_list) - 1 else body_img
        img_rotated = pygame.transform.rotate(img, dir)
        dis.blit(img_rotated, (x, y))

def message(msg, color):
    lines = msg.split('\n')
    y_offset = 0
    for line in lines:
        mesg = font_style.render(line, True, color)
        mesg_rect = mesg.get_rect(center=(dis_size / 2, dis_size / 2 + y_offset))
        dis.blit(mesg, mesg_rect)
        y_offset += font_style.get_linesize()

def gameLoop():
    global best_score

    game_over = False
    game_close = False

    x1 = dis_size / 2
    y1 = dis_size / 2
    x1_change = 0
    y1_change = 0
    direction = 0  # Initialisez direction avec une valeur par défaut, par exemple 0 pour droite.

    snake_List = [[x1, y1, direction]]
    Length_of_snake = 1

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
                    direction = 180
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

        dis.fill(dark_green)
        dis.blit(apple_img, (foodx, foody))

        # Assurez-vous que direction est définie
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

menu_principal()

