

from pygame import *
from random import randint

mixer.init()




font.init()
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial",80)
win = font2.render("YOU WIN!",True,(255,255,255))
lose = font2.render("YOU LOSE!",True,(180,0,0))

img_back = "forest.png"
img_hero = "(bow)gg.png"
img_enemy = "slaim2.png"
img_bos = "dragon3.png"
img_enemy3 = " slaim2.png"

score = 0
lost = 0
bos_life = 40
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bowByllet.png", self.rect.centerx, self.rect.centery-14, 15, 20, -15)
        bullets.add(bullet)

    #def bos_fire(self):
    #  bos_bullet = Bullet("faer_dol.png", self.rect.centerx, self.rect.centery-14, 15, 20, -15)
    #  bos_bullet.add(bos_bullet)
class Enemy(GameSprite ):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x <  0:
            self.rect.y = randint (150, win_height - 100)
            self.rect.x = 900
            lost +=1


class boser (GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x <  0:
            self.rect.y = 250
            self.rect.x = 900
            lost +=1000000
            bos_life = 100



class Asteroid(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_height:
            self.rect.y = randint (80, win_width - 80)
            self.rect.x = 0

class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()
goal = 100
max_lost = 10
win_width = 900
win_height = 500
life = 10

window = display.set_mode((win_width, win_height))
display.set_caption("zombie_tower.")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
boses = sprite.Group()
bos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 10 ):
    monster = Enemy(img_enemy, 900, randint(50, 400), 80, 50, randint(6, 10))
    monsters.add(monster)

bos = boser(img_bos, 900, 250, 200, 200, randint(1, 1))

run = True
finish = False
clock = time.Clock()
FPS = 40
rel_time = False
num_file =0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        text = font1.render("Рахунок" + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно:" + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font1.render (str(life),1,(255, 255, 255))
        window.blit(text_life, (600, 10))

        ship.update()
        monsters.update()
        boses.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        boses.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True,)

        for collides in collides :
            score += 1
            monster = Enemy(img_enemy, 900, randint(50, 400), 80, 50, randint(3, 6))
            monsters.add(monster)

        if sprite.spritecollide(bos,bullets,True):
            bos_life -= 1
            if bos_life < 0:
                score += 1000
                bos.kill()
        # for collide in collidess :
        #     bos_life -= 1
        #     if bos_life < 0 ():
        #         score  += 1000


        if score >= 50:
            bos.add(boses)

        if sprite.spritecollide(ship, monsters, False) :
            sprite.spritecollide(ship, monsters, True)
            monster = Enemy(img_enemy, 900, randint(50, 400), 80, 50, randint(3, 6))
            monsters.add(monster)
            life -= 1

        if sprite.collide_rect(ship, bos) :
            sprite.collide_rect(ship, bos, True)
            bos = boser(img_bos, 900, randint(50, 400), 80, 50, randint(3, 6))
            life -= 1000

        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose,(200,200))

        if  bos_life < 0 :
            finish = True
            window.blit(win , (200,200))

        display.update()

    clock.tick(FPS)


