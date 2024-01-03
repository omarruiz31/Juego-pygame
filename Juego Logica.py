import pygame
import sys
import random


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Atrapalo!!")

# Colores
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


background = pygame.image.load("fondo-3.jpg")  
background = pygame.transform.scale(background, (width, height))

trapper_image = pygame.image.load("canasta2.jpg").convert_alpha()  
trapper_rect = trapper_image.get_rect()
trapper_rect.topleft = (width // 2 - trapper_rect.width // 2, height - 100)


fruits = []

clock = pygame.time.Clock()
score = 0
fallen_fruits = 0

paused = False
game_over = False

def show_game_over():
    font = pygame.font.Font(None, 70)
    text = font.render("¡Game Over!", True, white)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused  

    if not (paused or game_over):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and trapper_rect.left > 0:
            trapper_rect.x -= 14

        if keys[pygame.K_RIGHT] and trapper_rect.right < width:
            trapper_rect.x += 14

        # Generar frutas aleatorias
        if random.randint(0, 100) < 5:
            fruit = pygame.Rect(random.randint(0, width - 20), 0, 20, 20)
            fruits.append(fruit)

        screen.blit(background, (0, 0))

        
        screen.blit(trapper_image, trapper_rect.topleft)

        for fruit in fruits[:]: 
            fruit.y += 8
            pygame.draw.ellipse(screen, blue, fruit)  

            
            if fruit.colliderect(trapper_rect):
                score += 1
                fruits.remove(fruit)

            # Eliminar frutas que llegan al suelo
            if fruit.bottom > height:
                fruits.remove(fruit)
                fallen_fruits += 1

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntuación: {score}", True, black) 
        screen.blit(score_text, (10, 10))

        # Mostrar frutas caídas
        fallen_text = font.render(f"Frutas Caídas: {fallen_fruits}", True, black)
        screen.blit(fallen_text, (width - fallen_text.get_width() - 10, 10))

        
        if fallen_fruits > 20:
            game_over = True

        
        pygame.display.flip()

       
        clock.tick(60)

    elif game_over:
        show_game_over()
        pygame.display.flip()
        pygame.time.wait(3000)  

        # Reiniciar el juego
        fruits = []
        trapper_rect.topleft = (width // 2 - trapper_rect.width // 2, height - 100)
        score = 0
        fallen_fruits = 0
        game_over = False

    if paused:
        
        font = pygame.font.Font(None, 50)
        text = font.render("¡Juego en Pausa!", True, white)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    screen.fill((0, 0, 0))
