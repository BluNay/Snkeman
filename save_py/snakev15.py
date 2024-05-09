import pygame
import random
import sys

pygame.init()

# Couleurs
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (92, 123, 53)
light_green = (138, 156, 78)
blue = (0, 0, 255)

# Paramètres de l'écran
dis_size = 600
dis = pygame.display.set_mode((dis_size, dis_size))
pygame.display.set_caption('Jeu de Serpent')

# Paramètres du serpent
snake_block = 20
snake_speed = 15

clock = pygame.time.Clock()

# Sons
pygame.mixer.init()
son_manger = pygame.mixer.Sound('sound/eat.wav')
son_collision = pygame.mixer.Sound('sound/collision.wav')

# Images
head_img = pygame.transform.scale(pygame.image.load('Images/Assets/head.png'), (snake_block, snake_block))
body_img = pygame.transform.scale(pygame.image.load('Images/Assets/body.png'), (snake_block, snake_block))
tail_img = pygame.transform.scale(pygame.image.load('Images/Assets/tail.png'), (snake_block, snake_block))
apple_img = pygame.transform.scale(pygame.image.load('Images/Assets/letchi_snake_game.png'), (snake_block, snake_block))

# Polices
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

best_score = 0

def your_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, (0, 0))

def best_score_display(score):
    value = score_font.render(f"Best Score: {score}", True, white)
    dis.blit(value, (0, 30))

def draw_snake(snake_list):
    for idx, seg in enumerate(snake_list):
        img = body_img if idx != 0 else pygame.transform.rotate(head_img, seg[2])
        dis.blit(img, (seg[0], seg[1]))

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_size / 2 - mesg.get_width() / 2, dis_size / 2 - mesg.get_height() / 2 + y_displace])

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
            message("Tu as perdu !", white, -50)
            message("Appuie sur 'C' pour rejouer ou 'Q' pour quitter", white, 50)
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
                game_over = True
            if event.type == pygame.KEYDOWN:
                x1_change, y1_change, direction = {
                    pygame.K_LEFT: (-snake_block, 0, 180),
                    pygame.K_RIGHT: (snake_block, 0, 0),
                    pygame.K_UP: (0, -snake_block, 90),
                    pygame.K_DOWN: (0, snake_block, -90),
                }.get(event.key, (x1_change, y1_change, direction))

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_size or x1 < 0 or y1 >= dis_size or y1 < 0:
            son_collision.play()
            game_close = True
            pygame.time.wait(500)

        dis.fill(dark_green)
        dis.blit(apple_img, (foodx, foody))
        snake_Head = [x1, y1, direction]

        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for seg in snake_List[:-1]:
            if seg[:2] == snake_Head[:2]:
                game_close = True

        draw_snake(snake_List)
        your_score(Length_of_snake - 1)
        best_score_display(best_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            son_manger.play()
            foodx = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_size - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            best_score = max(best_score, Length_of_snake - 1)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def menu_principal():
    menu = True
    while menu:
        dis.fill(dark_green)
        message("Appuyez sur 'Space' pour commencer ou 'Q' pour quitter", blue)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

menu_principal()
