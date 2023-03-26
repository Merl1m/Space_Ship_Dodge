'''
Space Dodge
Coded Orginally on Windows 10 pro platform by Mohammed Farhan NP
'''
#Import Section
import pygame
import random
import os

#pygame init
pygame.init()

#colors
black = (0,0,0)
green = (0,255,0)
white = (255,255,255)
red = (255,0,0)
orange = (255,165,0)
dark_green = (34,139,34)
blue = (0,0,205)

#variable
star_colors = [white,blue,dark_green,red,orange] 
SCREEN_SIZE = (800,830)
TITLE = "SPACE DODGE"
score = 0
enemy_list = pygame.sprite.Group()
space_ship_chance = 300
loop_count = 0
bomb_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()
powerup_chance = 5
missile_limit = 3
game_stat = 0
delay_time = 25
missile_list = pygame.sprite.Group()
game_count = 0
enemy_images = ["Enemy_1.png","Enemy_2.png","Enemy_3.png","Enemy_4.png"]
powerup_images = ["Graphics\Graphics_2\Powerup_red.png","Graphics\Graphics_2\Powerup_orange.png","Graphics\Graphics_2\Powerup_blue.png"]
speed = 4
stars_list = pygame.sprite.Group() 
#screen
window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(TITLE)

#classes
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics\Graphics_3\Player.png')
        self.lives = 3
        self.max_health = 200
        self.health = self.max_health
        self.rect = self.image.get_rect()
        
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Graphics\Graphics_1\{0}".format(random.choice(enemy_images)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(25,750,25)
        self.rect.y = 100
    
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5,10])
        self.image.fill(red)
        self.rect = self.image.get_rect()
    
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Powerup(pygame.sprite.Sprite):
    def __init__(self,color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.speed = 8
        if color == red:
            self.image = pygame.image.load(powerup_images[0])
        elif color == orange:
            self.image = pygame.image.load(powerup_images[1])
        elif color == blue:
            self.image = pygame.image.load(powerup_images[2])
            
        self.rect = self.image.get_rect()
    
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    
    def update(self):
        if self.rect.y < 800:
            self.rect.y += self.speed

class stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1,1])
        self.image.fill(random.choice(star_colors))
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.y += 3

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5,10])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y)) 

#function
def total_reset():
    global delay_time,count,speed
    delay_time = 25
    game_count = 0
    speed = 4

def game_speed_manage():
    global delay_time,game_count,speed
    if game_count == 2546:
        game_count = 0
        speed += 1
        if delay_time > 10:
            delay_time += -1    
    
def read_high_score():
    global high_score
    f = open("dist.txt","r")
    dist = f.readlines()
    for line in dist:
        try:
            line = int(line)
            high_score = line
            break
        except:
            pass

def draw_powerup():
    global powerup_list
    chance = random.randint(1,10000)
    colors = [red, orange, blue]
    
    if chance <= powerup_chance:
        p = Powerup(random.choice(colors))
        p.rect.x = random.randrange(25,751,25)
        p.rect.y = 100
        powerup_list.add(p)
    for p in powerup_list:
        if p.rect.y > 725:
            powerup_list.remove(p)
    for powerup in powerup_list:
        powerup.update()
        powerup.draw()

def enemy_draw():
    global loop_count, enemy_list, bomb_list,stars_list
    if loop_count == 5:
        loop_count = 0
        star = stars()
        star.rect.x = random.randrange(1,800)
        star.rect.y = 100
        stars_list.add(star)
        if chance < space_ship_chance:
            enemy = Enemy()
            enemy_list.add(enemy)
    
    for enemy in enemy_list:
        if enemy.rect.y > 700:
            enemy_list.remove(enemy)
        if enemy.rect.y < 700:
            enemy.rect.y += speed * 3
            enemy.draw()
        
    for enemy in enemy_list:
        if enemy.rect.x == ship.rect.x and enemy.rect.y < ship.rect.y:
            bomb = Bomb()
            bomb.rect.x = enemy.rect.x + 12.5
            bomb.rect.y = enemy.rect.y + 14
            bomb_list.add(bomb)
    
    for bomb in bomb_list:
        bomb.rect.y += speed * 5
        bomb.draw()
        if bomb.rect.y > 700:
            bomb_list.remove(bomb)            

def write(size,text,color,x,y):
    font = pygame.font.SysFont('Arial',size)
    main_text = font.render(text,False,color)
    main_text_rect = main_text.get_rect()
    main_text_rect.center = (x,y)
    window.blit(main_text,main_text_rect)



def score_stringate(main):
    score = main
    score_str = ''
    M_exists = False
    K_exists = False

    if score//1000000 >= 1:
        temp_1 = score// 1000000
        score = score - (temp_1 * 1000000)
        M_exists = True
        
    if score//1000 >= 1:
        temp_2 = score // 1000
        score = score - (temp_2 * 1000)
        K_exists = True

    if M_exists == True and K_exists == True:
        score_str = '{0}M {1}K {2}'.format(temp_1,temp_2,score)

    elif M_exists == True:
        score_str = '{0}M {1}'.format(temp_1,score)

    elif K_exists == True:
        score_str = '{0}K {1}'.format(temp_2,score)

    else:
        score_str = '{0}'.format(score)
    
    return score_str

def redraw():
    window.fill(black)
    for star in stars_list:
        star.update()
        if star.rect.y > 725:
            stars_list.remove(star)
    stars_list.draw(window)
    
    for hp in range(ship.health):
        pygame.draw.rect(window,red,(500 + (hp * 1.25),775,10,15))
    ship.draw()
    score_str = score_stringate(score)
    read_high_score()
    if score > high_score:
        highscore = score_stringate(score)
    else:
        highscore = score_stringate(high_score)
    write(28,'High_Score:{0}'.format(highscore),dark_green,700//1.1,25)
    enemy_draw()
    write(46,'Space Dodge',orange,700//2,25)
    bottom = pygame.draw.rect(window,green,(0,750,800,5))
    top = pygame.draw.rect(window,green,(0,100,800,5))
    write(28, 'Score:{0}'.format(score_str), white, 700//5, 25)
    life_string = '{0}x'.format(ship.lives)
    write(30,life_string,green,700//1.25,810)
    draw_powerup()
    for missile in missile_list:
        missile.rect.y += -speed * 3
        if missile.rect.y < 115:
            missile_list.remove(missile)
        missile.draw()
    pygame.display.update()

def start_loop():
    total_reset()
    global start_run,key_pressed,game_stat
    game_stat += 1 
    start_run = True
    while start_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_run = False
                key_pressed = 'q'
        window.fill(black)
        write(46,'Space Dodge',orange,700//2,25)
        write(35,'PRESS S TO CONTINUE...',orange,700//2,200)
        write(35,'PRESS Q TO QUIT',orange,700//2,300)
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            start_run = False
            key_pressed = 's'
        
        if key[pygame.K_q]:
            start_run = False
            key_pressed = 'q'
            
        pygame.display.update()


def main_loop():
    global score,key_pressed,enemy_list,bomb_list,powerup_list,run,loop_count,chance,game_count
    run = True
    if game_stat == 1:
        ship.lives = 3
    else:
        ship.lives = 4
    score = 0
    for e in enemy_list:
        enemy_list.remove(e)
    for p in enemy_list:
        powerup_list.remove(p)
    for b in bomb_list:
        bomb_list.remove(b)
    while run:
        game_count += 1
        loop_count += 1
        score += 1
        game_speed_manage()
        '''Game Handler'''
        pygame.time.delay(delay_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                key_pressed = 'q'

        chance = random.randint(1,1000)
        '''Key Binding'''
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            run = False
            key_pressed = 'q'

        if key[pygame.K_RIGHT]:
            ship.rect.x += 10
            if ship.rect.x > 750:
                ship.rect.x = 750
        if key[pygame.K_LEFT]:
            ship.rect.x += -10
            if ship.rect.x < 25:
                ship.rect.x = 25
        
        if key[pygame.K_SPACE]:
            if len(missile_list) < 3:
                missile = Missile()
                missile.rect.x = ship.rect.x + 17
                missile.rect.y = ship.rect.y
                missile_list.add(missile)
        
        '''collision'''
        for bomb in bomb_list:
            if bomb.rect.colliderect(ship.rect):
                ship.health += -5
                bomb_list.remove(bomb)
            for enemy in enemy_list:
                if bomb.rect.colliderect(enemy):
                    bomb_list.remove(bomb)
                    enemy_list.remove(enemy)
        for missile in missile_list:
            for enemy in enemy_list:
                if missile.rect.colliderect(enemy):
                    missile_list.remove(missile)
                    enemy_list.remove(enemy)
                
            for bomb in bomb_list:
                if missile.rect.colliderect(bomb):
                    missile_list.remove(missile)
                    bomb_list.remove(bomb)
                
        for enemy in enemy_list:
            if enemy.rect.colliderect(ship.rect):
                ship.health += -50
                enemy_list.remove(enemy)
        
        for powerup in powerup_list:
            if powerup.rect.colliderect(ship.rect):
                if powerup.color == red:
                    if ship.health < ship.max_health:
                        ship.health = ship.max_health
                
                if powerup.color == orange:    
                    ship.lives += 1
                
                if powerup.color == blue:
                    score += 10000
                
                powerup_list.remove(powerup)
            for enemy in enemy_list:
                if powerup.rect.colliderect(enemy.rect):
                    enemy_list.remove(enemy)
                
        if ship.health <= 0:
            ship.lives += -1
            ship.health = 200
        
        if ship.lives == 0:
            ship.health = 0
            run = False
        '''Screen Updater'''
        redraw()

#call sprites
ship = Ship()
ship.rect.x = 375
ship.rect.y = 650

#main functionalties of game
while True:
    start_loop()
    if key_pressed=='s':
        main_loop()
        if score > high_score:
            f = open("dist.txt","w+")
            f.write(str(score)+'\r\n')
            f.close()
            
    if key_pressed == 'q':
        break
    
#close window
pygame.quit()
