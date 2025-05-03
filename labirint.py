# Разработай свою игру в этом файле!
from pygame import *

RED = (255, 0, 0)
GREEN = (0, 255, 51)
BlUE = (0, 0, 255)
ORANGE = (255, 123, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (80, 80, 255)

speed_x_value = 10
speed_y_value = 10

window = display.set_mode((1000, 1000))
display.set_caption('Игра')
picture = transform.scale(image.load('cave.png'), (1000, 1000))
win = transform.scale(image.load('win.jpg'), (1000, 1000))
lose = transform.scale(image.load('game-over_1.png'), (1000, 1000))
win_width = 1000

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image_value = transform.scale(image.load(picture), (w, h))
        self.image = transform.scale(image.load(picture), (w, h))
        self.image_left = transform.flip(self.image_value, True, False)
        self.image_up = transform.rotate(self.image_value, 90)
        self.image_down = transform.rotate(self.image_value, 270)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, speed_x=0, speed_y=0):
        super().__init__(picture, w, h, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = 'right'
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        platforms_touced = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0:
            for p in platforms_touced:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0:
            for p in platforms_touced:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.speed_y > 0:
            for p in platforms_touced:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speed_y < 0:
            for p in platforms_touced:
                self.rect.top = max(self.rect.top, p.rect.bottom)
            
    
    def fire(self):
        bullet = Bullet('weapon.png', 15, 20, self.rect.right, self.rect.centery, 15, self.direction)
        bullets.add(bullet)

        

        

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 600:
            self.direction = 'right'
        if self.rect.x >= win_width - 125:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
            self.image = self.image_left
        else:
            self.rect.x += self.speed
            self.image = self.image_value

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed, direction):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = direction
    
    def update(self):
        if self.rect.x >= win_width:
            self.kill()
        if self.direction == 'right':
            self.rect.x += self.speed
            self.image = self.image_value
        elif self.direction == 'left':
            self.rect.x -= self.speed
            self.image = self.image_left
        elif self.direction == 'up':
            self.rect.y -= self.speed
            self.image = self.image_up
        elif self.direction == 'down':
            self.rect.y += self.speed
            self.image = self.image_down
        
            
            

        


wall = GameSprite('wall.png', 60, 300, 250, 500)
wall1 = GameSprite('wall.png', 300, 60, 250, 500)
wall2 = GameSprite('wall.png', 60, 300, 550, 260)
final = GameSprite('star.png', 100, 100, 800, 700)

player = Player('hero.png', 100, 100, 150, 700)
monster = Enemy('spider.png', 150, 150, 700, 300, 7)


barriers = sprite.Group()
barriers.add(wall, wall1, wall2)
bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(monster)
players = sprite.Group()
players.add(player)

run = True
finish = False

while run:
    time.delay(60)

    if player.rect.x <= 0:
        player.speed_x = 0
    if player.rect.y <= 0:
        player.speed_y = 0
    if player.rect.x >= 900:
        player.speed_x = 0
    if player.rect.y >= 900:
        player.speed_y = 0

    sprite.groupcollide(bullets, barriers, True, False)
    sprite.groupcollide(monsters, bullets, True, True)

    if sprite.groupcollide(monsters, players, False, True):
        finish = True
        window.blit(lose, (0, 0))

       

    for i in event.get():
        if i.type == QUIT:
          run = False
        if i.type == KEYDOWN:
            if i.key in (K_w, K_UP):
                player.speed_y = -speed_y_value
                player.direction = 'up'
            if i.key in (K_d, K_RIGHT):
                player.speed_x = speed_x_value
                player.image = player.image_value
                player.direction = 'right'
            if i.key in (K_a, K_LEFT):
                player.speed_x = -speed_y_value
                player.image = player.image_left
                player.direction = 'left'
            if i.key in (K_s, K_DOWN):
                player.speed_y = speed_x_value
                player.direction = 'down'
            if i.key == K_SPACE:
                player.fire()

        if i.type == KEYUP:
            if i.key in (K_w, K_UP):
                player.speed_y = 0
            if i.key in (K_d, K_RIGHT):
                player.speed_x = 0
            if i.key in (K_a, K_LEFT):
                player.speed_x = 0
            if i.key in (K_s, K_DOWN):
                player.speed_y = 0
         

    if finish != True:
        window.blit(picture, (0, 0))
        barriers.draw(window)
        players.draw(window)
        players.update()
        final.reset()
        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0, 0))



    display.update()