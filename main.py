import pygame
import random
import math
from pygame import mixer

#initialization of pygame
pygame.init()
mixer.music.load('background.wav')
mixer.music.play(-1)
#create the screen
screen=pygame.display.set_mode((800,600))

#title and icon
pygame.display.set_caption("Space Inviders")
icon=pygame.image.load('alien.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('space-invaders.png')
#(0,0) koordinate su gornji levi ugao
playerX=370
playerY=480 #y ide odozgo na dole
playerX_change=0

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

def init_enemy_coordinates():
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('ufo.png'))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(0.3)
        enemyY_change.append(40)

#bullet
bullet_state='ready' #ready-ne vidi se; fire-ispaljen i vidi se
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletY_change=1.5

#score
score_value=0
score_font=pygame.font.Font('ka1.ttf',28)
over_font=pygame.font.Font('ka1.ttf',64)
textX=10
textY=10

def game_over_text():
    over_text=over_font.render("Game over!",True,(255,255,255))
    screen.blit(over_text,(170,200))
    play_again_text=score_font.render("Play again?",True,(255,255,255))
    screen.blit(play_again_text,(300,300))

def show_score(x,y):
    score=score_font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y)) #blit-crtanje, ikonica i koordinate

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
    if distance<27:
        return True
    return False

init_enemy_coordinates()
#Game loop
#sve sto treba da se pojavljuje u prozoru stoji u while petlji
running=True
reset=False
while running:
    screen.fill((0,0,0))  # rgb-stoji tu jer se sve "crta" preko njega
    events=pygame.event.get() #hvata sve dogadjaje
    for event in events:
        #za zatvaranje
        if event.type==pygame.QUIT:
            running=False
        #KEYDOWN pritiskanje tastera
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.3
            if event.key==pygame.K_RIGHT:
                playerX_change=0.3
            if event.key==pygame.K_SPACE and bullet_state is 'ready':
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX=playerX
                fire_bullet(bulletX,bulletY)
        #KEYUP pustanje tastera
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

    #kretanje
    playerX+=playerX_change
    #granice
    if playerX<0:
        playerX=0
    elif playerX>736:
        playerX=736

    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY<0:
        bulletY=480
        bullet_state='ready'
    if bullet_state=='fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    #movements of player
    player(playerX,playerY)
    show_score(textX,textY)

    #da bi se konstantno apdejtovao widnow, pokreti i boje itd
    pygame.display.update()
