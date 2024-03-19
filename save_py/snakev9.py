import pygame
import random

# Initialisation de Pygame
pygame.init()

# Configuration initiale
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
clock = pygame.time.Clock()
snake_speed = 15

# Chargement des images
head_img = pygame.image.load('Images/Assets/head.png')
body_img = pygame.image.load('Images/Assets/body.png')
tail_img = pygame.image.load('Images/Assets/tail.png')
apple_img = pygame.image.load('Images/Assets/pomme.png')
background_img = pygame.image.load('Images/Assets/background.jpeg')

# Assurez-vous que vos assets sont de la taille appropriée
# Exemple: pygame.transform.scale(image, (20, 20))

# Police pour les scores
score_font = pygame.font.SysFont("comicsansms", 35)

best_score = 0  # Pour gérer le meilleur score

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, (255, 255, 102))
    dis.blit(value, [0, 0])

def best_score_display(score):
    value = score_font.render("Best Score: " + str(score), True, (255, 255, 255))
    dis.blit(value, [0, 30])

def our_snake(snake_list):
    for i, x in enumerate(snake_list):
        if i == 0:  # Queue
            dis.blit(tail_img, (x[0], x[1]))
        elif i == len(snake_list) - 1:  # Tête
            dis.blit(head_img, (x[0], x[1]))
        else:  # Corps
            dis.blit(body_img, (x[0], x[1]))

def gameLoop():
    global best_score

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = [[x1, y1 - 20], [x1, y1 - 10], [x1, y1]]  # Initialisation avec queue, corps, tête
    Length_of_snake = 3

    foodx = round(random.randrange(0, dis_width - snake_speed) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_speed) / 10.0) * 10.0

    while not game_over:
        # Gérer la fin du jeu et la réinitialisation ici
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # Ajouter la gestion des touches ici
        
        # Mettre à jour la position du serpent et vérifier les collisions ici

        dis.blit(background_img, (0, 0))
        dis.blit(apple_img, (foodx, foody))
        our_snake(snake_List)
        your_score(Length_of_snake - 3)  # -3 car le serpent commence avec 3 segments
        best_score_display(best_score)

        pygame.display.update()

        # Gérer le serpent mangeant une pomme ici

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
