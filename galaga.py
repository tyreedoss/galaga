# import libraries
import math
import random
import pygame
from pygame import mixer
import time


# create class for the player and enemy ships.
# attributes include x and y position and change
# in x and y
class ship:
    def __init__(self, sprite, xPos, yPos, deltaX, deltaY):
        self.sprite = sprite
        self.xPos = xPos
        self.yPos = yPos
        self.deltaX = deltaX
        self.deltaY = deltaY

    # update position by adding deltax/y
    # to x/y position
    def update_pos(self):
        self.xPos = self.deltaX + self.xPos
        self.yPos = self.deltaY + self.yPos


# initialize game
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load(r'.\img\background.png')
pygame.display.set_caption('Galaga')
# set player image, position and speed
playerImg = pygame.image.load(r'.\img\player_ship.png')
player = ship(playerImg, 400, 530, 0, 0)


# set enemy image, positions, and speed
enemyImg = pygame.image.load(r'.\img\enemy_ship.png')
enemy = []
enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 0, 0.15))
speedx = 0
num_enemies = 1
# set bullet image, positions, and speed
bulletImg = pygame.image.load(r'.\img\bullet.png')
bulletX = 0
bulletY = 530
bulletX_change = 0
bulletY_change = 20
# indicates status of bullet (ready = not fired)
# (fired = shot)
bullet_state = 'ready'
# wildShip is a ship that will randomly spawn
# and move straight down
wildShipImg = pygame.image.load(r'.\img\wild_ship.png')
wildShip = ship(wildShipImg, 400, -100, 0, 0)


# print player ship on screen
def print_player(x, y):
    screen.blit(playerImg, (x, y))


# print each individual enemy ship on screen
def print_enemy(x, y, n):
    screen.blit(enemy[n].sprite, (x, y))


# print bullet on screen
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


# check if bullet hit enemy
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 35:
        return True
    else:
        return False


# initialize score and score text
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
lose_font = pygame.font.Font('freesansbold.ttf', 64)
controls_font = pygame.font.Font('freesansbold.ttf', 16)
instructions = """Controls: W = Up; A = Left; S = Down; D = Right; Spacebar = Shoot"""
textX = 10
textY = 10
# flags
flag = 2
flag2 = 2
flag3 = 2
flag4 = 2
wildcard = 0


# function to display score text
def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x,y))


# display game over text
def game_over_text():
    lose_text = lose_font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(lose_text, (200, 250))


# display controls
def controls(x, y):
    controls_text = controls_font.render(instructions, True, (255, 255, 255))
    screen.blit(controls_text, (x, y))


# player horizontal boundaries
def player_x(x):
    if x <= 0:
        x = 0
    if x >= 736:
        x = 736
    return x


# player vertical boundaries
def player_y(y):
    if y <= 0:
        y = 0
    if y >= 536:
        y = 536
    return y


# to temporarily display controls
start = time.time()
disp_controls = True
# create infinite loop
running = True
while running:
    # background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    if disp_controls:
        controls(150, 400)
    else:
        controls(150, -100)
    # loop through all possible events
    for event in pygame.event.get():
        # stop program if close button is clicked
        if event.type == pygame.QUIT:
            running = False
        # move up if 'w' is pressed, down if 's' is pressed, left
        # for 'a', and right for 'd'. shoot with spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.deltaY = -3.5
            if event.key == pygame.K_a:
                player.deltaX = -6
            if event.key == pygame.K_s:
                player.deltaY = 3.5
            if event.key == pygame.K_d:
                player.deltaX = 6
            if event.key == pygame.K_SPACE:
                # play laser sound when shooting
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound(r'.\sfx\laser.wav')
                    bullet_sound.play()
                    bulletX = player.xPos
                    bulletY = player.yPos
                    fire_bullet(bulletX, bulletY)
                else:
                    continue
        # stop moving if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.deltaY = 0
            if event.key == pygame.K_a:
                player.deltaX = 0
            if event.key == pygame.K_s:
                player.deltaY = 0
            if event.key == pygame.K_d:
                player.deltaX = 0
    # makes the player ship move
    player.update_pos()
    # loop through the number of enemies current
    for n in range(num_enemies):
        # show game over text if enemy reaches bottom
        # of screen
        if enemy[n].yPos >= 540:
            for j in range(num_enemies):
                enemy[j].yPos = 2000
            game_over_text()
            break

        # if there is one guy, he will just move down
        if num_enemies < 2:
            enemy[n].deltaX = 0
            enemy[n].deltaY = 1
            # enemy[n].update_pos()
        # multiple enemies:
        else:
            # first enemy will no longer move vertically
            enemy[0].deltaY = 0
            # each round, indicated by flag,
            # x-speed changes
            if flag != 0:
                enemy[n].deltaX = 1
                speedx = 1
                flag -= 1
            if flag2 == 1:
                enemy[n].deltaX = 2
                speedx = 2
                flag2 -= 1
            if flag3 == 1:
                enemy[n].deltaX = 3
                speedx = 3
                flag3 -= 1
            if flag4 == 1:
                enemy[n].deltaX = 4
                speedx = 4
                flag4 -= 1
            # if random number between 1 and 5 is
            # 2, then the wildShip will move down
            # the screen
            if wildcard == 2:
                wildShip.deltaX = 0
                wildShip.deltaY = 1
            # if an enemy reaches left boundary, reverse x-direction
            # and move down
            if enemy[n].xPos <= 0:
                enemy[n].deltaX = -enemy[n].deltaX
                enemy[n].yPos += 20
            # if an enemy reaches right boundary, reverse x-direction
            # and move down
            elif enemy[n].xPos >= 736:
                enemy[n].deltaX = -enemy[n].deltaX
                enemy[n].yPos += 20
        # collision will be a boolean depending on if
        # bullet hits target
        collision = is_collision(enemy[n].xPos, enemy[n].yPos, bulletX, bulletY)
        # if enemy is hit
        if collision:
            # play explosion sound
            explosion_sound = mixer.Sound(r'.\sfx\explosion.wav')
            explosion_sound.play()
            # return bullet to ship, set state to ready,
            # increase score
            bulletY = player.yPos
            bullet_state = 'ready'
            score_val += 1
            # every 15 points, add new enemy that moves
            # horizontally
            if score_val % 15 == 0:
                pass
                if flag == 2:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 1, 0))
                    flag -= 1
                else:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 1, 0))
                num_enemies += 1
            # every 30 points, add enemy that diagonal
            if score_val % 32 == 0:
                pass
                if flag2 == 2:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 2, 0.5))
                    flag2 -= 1
                else:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 2, 0.5))
                num_enemies += 1
            # faster
            if score_val % 62 == 0:
                pass
                if flag3 == 2:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 3, 0.7))
                    flag3 -= 1
                else:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 3, 0.7))
            # very fast
            if score_val % 82 == 0:
                pass
                if flag4 == 2:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 4, 1))
                    flag4 -= 1
                else:
                    enemy.append(ship(enemyImg, random.randint(0, 536), random.randint(0, 100), 4, 1))
                num_enemies += 1
            # reset position
            enemy[n].xPos = random.randint(0, 536)
            enemy[n].yPos = random.randint(0, 100)
            # if more than one enemy, and there is not
            # already a wildship, new wildcard
            if num_enemies > 1 and wildcard != 2:
                wildcard = random.randint(1, 5)
        # check if bullet hit wildship
        wildShipHit = is_collision(wildShip.xPos, wildShip.yPos, bulletX, bulletY)
        # if true
        if wildShipHit:
            # play sound
            explosion_sound = mixer.Sound(r'.\sfx\explosion.wav')
            explosion_sound.play()
            # reset bullet
            bulletY = player.yPos
            bullet_state = 'ready'
            score_val += 1
            # reset position, speed, and card
            wildShip.xPos = random.randint(0, 536)
            wildShip.yPos = -100
            wildShip.deltaX = 0
            wildShip.deltaY = 0
            wildcard = 0
        # print enemies to screen and update positions
        print_enemy(enemy[n].xPos, enemy[n].yPos, n)
        enemy[n].update_pos()
    screen.blit(wildShipImg, (wildShip.xPos, wildShip.yPos))
    wildShip.update_pos()
    # game over if wildship reach bottom
    if wildShip.yPos >= 540:
        wildShip.yPos = 2000
        for j in range(num_enemies):
            enemy[j].yPos = 2000
        game_over_text()
    # borders for the player
    player.xPos = player_x(player.xPos)
    player.yPos = player_y(player.yPos)
    # bullet movement
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 530
        bullet_state = 'ready'
    print_player(player.xPos, player.yPos)
    show_score(textX, textY)
    pygame.display.update()
    # remove controls text after 10 sec
    stop = time.time()
    elapsed = stop - start
    if elapsed > 10:
        disp_controls = False
