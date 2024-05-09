import pygame
import random
import sys

pygame.init()

white = (255, 255, 255)
red = (213, 50, 80)
dark_green = (92, 123, 53)
light_green = (138, 156, 78)
blue = (50, 153, 213)

dis_size = 600
dis = pygame.display.set_mode((dis_size, dis_size))
pygame.display.set_caption('Jeu de Serpent')

snake_block = 20
snake_speed = 15

clock = pygame.time.Clock()

pygame.mixer.init()
son_manger = pygame.mixer.Sound('sound/eat.wav')
son_collision = pygame.mixer.Sound('sound/collision.wav')

head_img = pygame.image.load('Images/Assets/head.png').convert_alpha()
body_img = pygame.image.load('Images/Assets/body.png').convert_alpha()
tail_img = pygame.image.load('Images/Assets/tail.png').convert_alpha()
apple_img = pygame.image.load('Images/Assets/letchi_snake_game.png').convert_alpha()

head_img = pygame.transform.scale(head_img, (snake_block, snake_block))
body_img = pygame.transform.scale(body_img, (snake_block, snake_block))
tail_img = pygame.transform.scale(tail_img, (snake_block, snake_block))
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

best_score = 0

def draw_button(text, center_x, center_y):
    font = pygame.font.SysFont("bahnschrift", 35)
    text_surf = font.render(text, True, white)
    text_rect = text_surf.get_rect(center=(center_x, center_y))
    button_rect = pygame.draw.rect(dis, blue, text_rect.inflate(20, 10), 2)
    dis.blit(text_surf, text_rect)
    return button_rect

def menu_principal():
    menu = True
    while menu:
        dis.fill(dark_green)
        start_button = draw_button("Commencer", dis_size // 2, dis_size // 2 - 50)
        quit_button = draw_button("Quitter", dis_size // 2, dis_size // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    gameLoop()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def draw_snake(snake_list):
    for i, seg in enumerate(snake_list):
        if i == 0:  # Tête
            img = pygame.transform.rotate(head_img, seg[2])
        elif i == len(snake_list) - 1:  # Queue, pas de rotation pour simplifier
            img = tail_img
        else:  # Corps
            img = body_img
        dis.blit(img, (seg[0], seg[1]))

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

    foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            dis.fill(red)
            message("Tu as perdu ! Appuie sur 'C' pour rejouer ou 'Q' pour quitter", white)
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
                game_over = True
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
            pygame.time.wait(500)

        dis.fill(dark_green)

        dis.blit(apple_img, (foodx, foody))

        snake_Head = [x1, y1, direction]

        if len(snake_List) > 1:
            snake_List.insert(1, snake_Head)  # Ajoute un nouveau segment de corps juste derrière la tête
            if len(snake_List) > Length_of_snake:
                del snake_List[-1]  # Supprime le dernier segment du corps pour garder la taille constante
        else:
            snake_List.append(snake_Head)  # Pour le premier aliment mangé

        if x1 == foodx and y1 == foody:
            son_manger.play()
            foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            best_score = max(best_score, Length_of_snake - 1)

        draw_snake(snake_List)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

menu_principal()
