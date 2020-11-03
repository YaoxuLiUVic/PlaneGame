#  File:       Game.py 
#  Purpose:    Using object oriented thinking to design a plane fight game
#  Programmers:Yaoxu Li (120A)
#  Team:       Romantic Programmers
#
#  Course:     CSCI120
#  Date:       Snday 9th December 2018, 21:05 PT
#  References: http://inventwithpython.com/pygame/
#              http://inventwithpython.com/makinggames.pdf
#              https://pythonprogramming.net/pygame-button-function-events/




import pygame
import sys
import random
import time

#initialize pygame
pygame.init()
pygame.mixer.init()
#set windows size
bg_size = WIDTH, HEIGHT = 800, 490

#load images
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("image/Destiny in the Pacific")
background = pygame.image.load("image/Back.png")
background2 = pygame.image.load("image/Back2.png")
intro = pygame.image.load("image/intro2.png")
plane_img = pygame.image.load("image/USAPlane.png")
plane_img2 = pygame.image.load("image/JapPlane.png")
enemy_img = pygame.image.load("image/Enemy1.png")
enemy_img2 = pygame.image.load("image/Enemy2.png")
bullet_image = pygame.image.load("image/Bullet.png")
explosion = pygame.image.load("image/explosion.png")
start = "image/start.png"
start2 = "image/start2.png"
zi = pygame.image.load("image/zi.png")
des = pygame.image.load("image/destiny.png")
Allies = "image/Allies.png"
Allies2 = "image/Allies2.png"
Axis = "image/JG.png"
Axis2 = "image/JG2.png"
exit_img = "image/exit.png"
exit_img2 = "image/exit2.png"
bullet_image = pygame.image.load("image/Bullet.png")
gameOver = pygame.image.load("image/Over.png")
Sea = pygame.image.load("image/Sea.png")
screen.blit(background, (0, 0))
screen.blit(zi, (60,50))
screen.blit(des, (100,150))

#global variables
shootDelay = 0
player_shoot = 0
score = 0
FRE = 0

#button class
class Button(object):
    def __init__(self,up,down,position):
        self.imageUp = pygame.image.load(up).convert_alpha()
        self.imageDown = pygame.image.load(down).convert_alpha()
        self.position = position
        self.state = False

    # check if the mouse is on the button
    def pos(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position

        # check if click
        if self.pos():
            screen.blit(self.imageDown, (x-w/2,y-h/2))
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.state = True
        else:
            screen.blit(self.imageUp, (x-w/2, y-h/2))


#bullet class           
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, bullet_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = bullet_position
        self.move = 1.1

    def bulletMove(self):
        self.rect.top -= self.move

#player class   use pygame.sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, player_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = plane_img
        self.rect = self.image.get_rect()
        self.rect.topleft = player_position
        self.move = 5
        self.bullets = pygame.sprite.Group()
        self.is_hit = False

    #move   has a limitaion
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.move

    def moveDown(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        else:
            self.rect.bottom += self.move

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.move

    def moveRight(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        else:
            self.rect.right += self.move

    # shoot
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
       # shootMusic.play()

#enemy class    use pygame.sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemyShot_img, enemy_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_position
        self.shot_img = enemyShot_img
        self.move = 1
        self.shot_index = 0

    def enemyMove(self):
        self.rect.top += self.move


#create buttons
button = Button(start,start2,(400,300))
button2 = Button(Allies,Allies2,(230,320))
button3 = Button(Axis,Axis2,(570,320))

#main function
def main():
    global FRE
    global plane_img
    global player_shoot
    global score
    global shootDelay
    global enemy_img

    #back ground music
    pygame.mixer.music.load('music/bgm2.mp3')
    pygame.mixer.music.play(-1)

    #game loop
    running = True
    while running:

        #start button
        button.render()
        if button.state == True:
            screen.blit(background2, (0, 0))
            screen.blit(intro, (50, 30))
            button2.render()
            button3.render()


        # button2 and button3 allow player to choose different group   
        if button2.state == True:
            screen.blit(Sea, (0, 0))
        if button3.state == True:
            screen.blit(Sea, (0, 0))
            plane_img = plane_img2
            enemy_img = enemy_img2

        #click the button, then enter the game
        if(button2.state == True or button3.state == True):

            #set infromation of objects
            player_position = [370, 370]
            player_rect = pygame.Rect(0,0,120,120)
            player = Player(plane_img, player_rect, player_position)
            bullet_rect = pygame.Rect(0, 0, 10, 10)
            enemy_rect = pygame.Rect(0, 0, 120, 120)
            enemies_shot_img = explosion
            enemies = pygame.sprite.Group()
            enemies_shot = pygame.sprite.Group()

            RUN = True

            while RUN:
                screen.blit(Sea, (0, 0))
                if not player.is_hit:
                    screen.blit(player.image, player.rect)
                #if player hit enemy
                else:
                    screen.blit(explosion, player.rect)
                    player_shoot += 31
                    if player_shoot >= 0:
                        RUN = False
                        running = False
                        time.sleep(1)

                #control the frecuency of enemies
                if FRE % 300 == 0:
                    enemy_position = [random.randint(0, WIDTH - enemy_rect.width), 0]
                    enemy = Enemy(enemy_img, enemies_shot_img, enemy_position)
                    enemies.add(enemy)
                FRE +=2
                if FRE == 1000:
                    FRE = 0
                for bullet in player.bullets:
                    bullet.bulletMove()
                    #delete bullet if out of window
                    if bullet.rect.bottom <= 0:
                        player.bullets.remove(bullet)

                player.bullets.draw(screen)

                #check collision
                for enemy in enemies:
                    enemy.enemyMove()
                    if pygame.sprite.collide_circle_ratio(0.6)(player, enemy):
                        enemies_shot.add(enemy)
                        enemies.remove(enemy)
                        player.is_hit = True
                        break

                #delete enemy if enemy is out of window
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)

                #check collision
                for enemy_shot in enemies_shot:
                    if enemy_shot.shot_index == 0:
                        pass
                    if enemy_shot.shot_index > 70:
                        enemies_shot.remove(enemy_shot)
                        score += 100
                        continue
                    screen.blit(enemy_shot.shot_img, enemy_shot.rect)
                    enemy_shot.shot_index += 1
                enemies.draw(screen)

                enemies_is_shot = pygame.sprite.groupcollide(enemies, player.bullets, 0.6, 0.8)

                for enemy_shot in enemies_is_shot:
                    enemies_shot.add(enemy_shot)

        
                # display score
                score_font = pygame.font.Font(None, 56)
                score_text = score_font.render("Your score:"+str(score), True, (128, 12, 12))
                text_rect = score_text.get_rect()
                text_rect.topleft = [10, 10]
                screen.blit(score_text, text_rect)


                #get command from keyboard
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                    player.moveUp()
                if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                    player.moveDown()
                if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                    player.moveLeft()
                if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                    player.moveRight()
                if key_pressed[pygame.K_SPACE]:
                    # set a delay in shooting   avoid shooting too fast
                    if shootDelay % 80 == 0:
                        player.shoot(bullet_image)
                    shootDelay += 5
                    if shootDelay >= 80:
                        shootDelay = 0
                #quit              
                for event in pygame.event.get():  # 
                    if event.type == pygame.QUIT:  # 
                        pygame.quit()
                        sys.exit()
                pygame.display.update()


        #quit
        for event in pygame.event.get():  # 
            if event.type == pygame.QUIT:  # 
                pygame.quit()
                sys.exit()
                 
        pygame.display.flip()
        pygame.display.update()

        
    if not running:
        pygame.mixer.music.stop()
        screen.blit(gameOver, (100,100))
        pygame.display.update()
        while True:

            #create a quit button
            button4 = Button(exit_img,exit_img2,(400,300))
            button4.render()
            pygame.display.update()
            if button4.state == True:
                pygame.quit()
                sys.exit()
            for event in pygame.event.get():  # 
                if event.type == pygame.QUIT:  # 
                    pygame.quit()
                    sys.exit()
        
# call main
main()

