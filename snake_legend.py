import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Legend 👑🐍")
clock = pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
DARK_GREEN = (0,180,0)
RED = (255,0,0)
BLUE = (0,150,255)
WHITE = (255,255,255)
GRAY = (120,120,120)

font = pygame.font.SysFont("Arial", 22)

# Ovoz
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
except:
    eat_sound = None

def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt","r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open("highscore.txt","w") as f:
        f.write(str(score))

def random_pos():
    return [random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)]

def game():
    snake = [[100,100]]
    direction = [BLOCK,0]
    food = random_pos()
    bombs = [random_pos() for _ in range(2)]
    walls = [[200,200],[220,200],[240,200],[260,200]]

    score = 0
    level = 1
    speed = 10
    highscore = load_highscore()

    while True:
        clock.tick(speed)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != [0,BLOCK]:
                    direction = [0,-BLOCK]
                if event.key == pygame.K_s and direction != [0,-BLOCK]:
                    direction = [0,BLOCK]
                if event.key == pygame.K_a and direction != [BLOCK,0]:
                    direction = [-BLOCK,0]
                if event.key == pygame.K_d and direction != [-BLOCK,0]:
                    direction = [BLOCK,0]

        head = [snake[0][0]+direction[0],
                snake[0][1]+direction[1]]

        if (head in snake or
            head in bombs or
            head in walls or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT):

            if score > highscore:
                save_highscore(score)

            screen.fill(BLACK)
            msg = font.render("GAME OVER! Press R", True, RED)
            screen.blit(msg,(WIDTH//3, HEIGHT//2))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game()
                clock.tick(5)

        snake.insert(0, head)

        if head == food:
            score += 1
            if eat_sound:
                eat_sound.play()
            if score % 5 == 0:
                level += 1
                speed += 2
                bombs.append(random_pos())
            food = random_pos()
        else:
            snake.pop()

        for w in walls:
            pygame.draw.rect(screen, GRAY, (*w,BLOCK,BLOCK))

        for b in bombs:
            pygame.draw.rect(screen, BLUE, (*b,BLOCK,BLOCK))

        pygame.draw.rect(screen, RED, (*food,BLOCK,BLOCK))

        for i, part in enumerate(snake):
            color = GREEN if i==0 else DARK_GREEN
            pygame.draw.rect(screen,color,(*part,BLOCK,BLOCK))

        screen.blit(font.render(f"Score: {score}", True, WHITE),(10,10))
        screen.blit(font.render(f"Level: {level}", True, WHITE),(10,35))
        screen.blit(font.render(f"HighScore: {highscore}", True, WHITE),(10,60))

        pygame.display.update()

game()