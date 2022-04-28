import pygame
import random
import math

pygame.init()

# Create the screen, title and icons
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
backgound = pygame.image.load("universe.png")

#Variables for Player
playerImg = pygame.image.load("player.png")
playerx = 400
playery = 450
playerchange = 0


#Variables for Enemies
enemyImg = []
enemyx = []
enemyy = []
enemychangex = []
enemychangey = []
totalenemies = 5

for i in range(totalenemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyx.append(random.randint(100, 700))
    enemyy.append(random.randint(300, 400))
    enemychangex.append(2)
    enemychangey.append(20)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletchangey = -10
fire = False

#counts number of enemies hit
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textx = 10
texty = 10

def show_score(x,y):
    fscore = font.render("Score : " + str(score), True, (0,0,255))
    screen.blit(fscore, (x, y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    if fire:
        screen.blit(bulletImg, (x, y + 10))

def distance(px, py, qx, qy):
    dx = math.pow(qx-px, 2)
    dy = math.pow(qy-py, 2)
    return math.sqrt(dx + dy)

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    dist = distance(enemy_x, enemy_y, bullet_x, bullet_y)
    if dist < 30:
        return True
    return False

def gameover():
    overfont = pygame.font.Font("freesansbold.ttf", 44)
    over = overfont.render("Game Over", True, (255,0,0))
    screen.blit(over, (200,250))

run = True
arrow_keys = [pygame.K_LEFT, pygame.K_RIGHT]

while run:
    # exits the window if the close button is clicked
    screen.fill((0,0,0))
    screen.blit(backgound, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == arrow_keys[0]:
                playerchange = -2
            elif event.key == arrow_keys[1]:
                playerchange = 2
            elif event.key == pygame.K_SPACE:
                bulletx = playerx
                if bullety < 0:
                    bullety = playery
                if not fire:
                    fire = True
                    fire_bullet(playerx, bullety)
        elif event.type == pygame.KEYUP:
            if event.key in arrow_keys:
                playerchange = 0

    #player move
    if playerx < 0:
        playerx = 0
        playerchange = 0
    elif playerx > 764:
        playerx = 764
        playerchange = 0
    else:
        playerx += playerchange

    #intial move enemy
    for i in range(totalenemies):
        if is_collision(enemyx[i], enemyy[i], playerx, playery):
            for j in range(totalenemies):
                enemychangex = 0
                enemychangey = 0
            gameover()
            break
            
        enemyx[i] += enemychangex[i]

        if enemyx[i] > 764 or enemyx[i] < 0:
            enemychangex[i] *= -1
            enemyx[i] += enemychangex[i]
            enemyy[i] += enemychangey[i]

        if enemyy[i] > 500 or enemyy[i] < 0:
            enemyy[i] -= enemychangey[i]
            enemychangey[i] = -enemychangey[i]



    #bullet movement
        if fire:
            fire_bullet(playerx, bullety)
            bullety += bulletchangey

    # collision
        colided = is_collision(enemyx[i], enemyy[i], bulletx, bullety)
        if colided == True:
            score += 1
            print(score)
            bullety = 480
            fire = not fire
            enemyx[i] = random.randint(100, 700)
            enemyy[i] = random.randint(10, 200)
        enemy(enemyx[i], enemyy[i],i)
    
    show_score(textx, texty)
    player(playerx, playery)
    pygame.display.update()
