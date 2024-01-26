from pygame import *
from random import randint
#звук
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire = mixer.Sound("fire.ogg")
#зображення
class GameSprite(sprite.Sprite):
    

    def __init__(self, player_image, player_speed, player_x, player_y, width, hight ):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width, hight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def recet(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        #if keys_pressed[K_UP] and self.rect.y > 7:
            #self.rect.y -= self.speed

        #if keys_pressed[K_DOWN] and self.rect.y < win_height - 50:
            #self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', -15,   self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)


#лічильник збитих і пропущених кораблів
    
score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 



        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

#ігрова сцена
            
window = display.set_mode((700, 500))
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"),(win_width, win_height))

#шрифти
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

txt_lose_game = font1.render('YOU LOSE', True, [255, 0, 0])
txt_win_game = font1.render('YOU WIN', True, [0, 255, 0])

#спрайти
rocket = "rocket.png"
bullet = "bullet.png"
asteroid ="asteroid.png"
ufo = "ufo.png"

rocket = Player("rocket.png", 13, win_height - 100, 400, 80, 100)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(ufo, randint(1, 5),randint(80, win_width - 80), -35, 80, 50)
    monsters.add(monster)
#змінна гра закінчилась

finish = False

#основний цикл
run = True

while run:

    #подія натискання на кнопку закрити 
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    if not finish:
        window.blit(background, (0, 0))       
        #пишемо текст на екрані
        text = font2.render("Рахунок:" +str(score), 1, (255, 255, 255)) 
        window.blit(text, (10, 20))
        text = font2.render("Пропущено:" +str(lost), 1, (255, 255, 255)) 
        window.blit(text, (10, 50))
        #рухи спрайтів
        rocket.update()
        rocket.recet()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        if sprite.spritecollide(rocket, monsters, False):
            finish = True 
            window.blit(txt_lose_game, [200, 200])

    #if sprite.spritecollide(rocket, monsters, True):
        #finish = True 
        #window.blit(txt_win_game, [200, 200])

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            monster = Enemy(ufo, randint(1, 5),randint(80, win_width - 80), -35, 80, 50)
            monsters.add(monster)
            score += 1

        if score == 10:
            finish = True
            window.blit(txt_win_game, [200, 200])

        if lost == 5:
            finish = True
            window.blit(txt_lose_game, [200, 200])

        display.update()
    else:
        score = 0
        lost = 0
        finish = False

        for m in monsters:
            m.kill()


        for m in bullets:
            m.kill()    
   
    #clock.tick(FPS)

        time.delay(3000) 
        for i in range(1, 5):
            monster = Enemy(ufo, randint(1, 5),randint(80, win_width - 80), -35, 80, 50)
            monsters.add(monster)
    time.delay(50)
