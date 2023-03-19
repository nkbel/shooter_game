from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win =  font2.render("YOU WIN!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!", True, (180, 0, 0))
lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


rocket = Player("rocket.png", 350, 400, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 2))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

clock = time.Clock()
FPS = 60
game = True
finish = False
max_lost = 5
goal = 10
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
                
    if not finish:
        window.blit(background, (0, 0))
        text = font1.render("Счёт:" + str(score), 1, (255,255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render("Пропущено" + str(lost), 1, (255,255, 255))
        window.blit(text_lose, (10, 50))

        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
    
    
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay (3000)
        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy("asteroid.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 2))
            asteroids.add(asteroid)     
        
        
    
    





    clock.tick(FPS)
    display.update()