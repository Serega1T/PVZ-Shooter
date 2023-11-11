from pygame import *
from random import *

#classes


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, img_x, img_y, character):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (img_x, img_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.char = character
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):      
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 1150:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_k]:
            self.char = "korn"
            self.image = transform.scale(image.load("kerner.png"), (90, 90))
        if keys_pressed[K_p]:
            self.char = "peach"
            self.image = transform.scale(image.load("rocket.png"), (110, 90))
        if keys_pressed[K_s]:
            self.char = "ice"
            self.image = transform.scale(image.load("ice.png"), (90, 90))

    
             
    def speed(self):
        self.speed = 8 
            
    def fire(self):
        if self.char == "korn":
            pbullets.add(Bullet("kornb.png", self.rect.centerx, self.rect.top, -10, 40, 40, "1"))
        elif self.char == "peach":
            pbullets.add(Bullet("bullet.png", self.rect.centerx, self.rect.top, -10, 40, 40, "2"))
        elif self.char == "ice":
            pbullets.add(Bullet("iceb.png", self.rect.centerx, self.rect.top, -10, 40, 40, "3"))
b = ["bullet.png","iceb.png","kornb.png"]
lost = 0
kill = 0
blast = 0
class UFO(GameSprite):
    def update(self):
        global lost

        if self.rect.y <= 720:
            self.rect.y += self.speed

        else:
            self.rect.x = randint(0, 640)
            self.rect.y = randint(-200, 0)
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<=-10:
            self.kill()
        
#window-creation


window = display.set_mode((1280, 720))
display.set_caption('PVZ-Shooter')
background = transform.scale(image.load("galaxy.jpg"), (1280, 720))
window.blit(background, (0, 0))
a = randint(70,250)*-1
hero = Player("rocket.png", 50, 630, 4, 90, 90, "peach")
score = Player("score.png", 1100, 600, 0, 100, 90, "score")
monsters = sprite.Group()

pbullets = sprite.Group()
heroes = sprite.Group()
heroes.add(hero)
a = ["ufo.png","ufo1.png","ufo2.png","ufo3.png"]
for i in range(7):
    monster = UFO(a[randint(0,3)], randint(0, 1180), randint(-400, 0), randint(1,2), 90, 110, "ufo")
    monsters.add(monster)

#cycle-game
clock = time.Clock()
clock.tick(60)

game = True
finish = False

scorest = 1
killscr = 1

mixer.init()
mixer.music.load('grasswalk.ogg')
mixer.music.play()

hit = mixer.Sound('hit.ogg')
throw = mixer.Sound('Throw.ogg')
loser = mixer.Sound('lose.ogg')
winer = mixer.Sound('win.ogg')

font.init()
font = font.SysFont('Arial', 30)
win = font.render('You Win!', True, (255,215,0))
lose = font.render('You Lose!', True, (255,0,0))
while game:
    display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYUP:
            if e.key == K_SPACE:
                throw.play()
                blast += scorest  
                hero.fire()

           
       
    if finish != True:
        window.blit(background, (0, 0))
        sprites_list = sprite.groupcollide(monsters, pbullets, True, True)
        for i in sprites_list:
            hit.play()
            kill += killscr
            monster = UFO(a[randint(0,3)], randint(200, 1000), randint(-400, 0), randint(1,2), 90, 110, "ufo")
            monsters.add(monster)
        sprites_list2 = sprite.groupcollide(heroes, monsters, False, True)
        for i in sprites_list2:
            mixer.music.stop()
            loser.play()
            finish = True

        pbullets.update()
        pbullets.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.update()
        hero.reset()
        score.reset()

        lostsch = font.render("Пропущено: " + str(lost), 1 , (255, 255, 255))
        window.blit(lostsch, (20, 20))
        blasting = str(blast)
        a1 = font.render("Цель: ", 1 , (255, 255, 255))
        window.blit(a1, (20, 120))
        a2 = font.render("- Убить 50 зомби " + str(kill) + "/50", 1 , (255, 255, 255))
        window.blit(a2, (20, 150))
        a3 = font.render("- Сделать 70 выстрелов " + str(blast) + "/70", 1 , (255, 255, 255))
        window.blit(a3, (20, 180))

        

        killsch = font.render("" + str(kill), 1 , (255, 0, 0))
        window.blit(killsch, (1220, 660))
        killsch = font.render("Счёт выстрелов: " + str(blast), 1 , (255, 0, 255))
        persona1 = font.render("[P] - Горохострел", 1 , (0, 51, 0))
        window.blit(persona1, (1000, 100))
        persona2 = font.render("[K] - Зернопульта", 1 , (255, 255, 0))
        window.blit(persona2, (1000, 50))
        persona3 = font.render("[S] - Снегострел", 1 , (0, 0, 255))
        window.blit(persona3, (1000, 150))

        keys_pressed = key.get_pressed()
        if blast >= 70:
            scorest = 0 
            a3 = font.render("- Сделать 70 выстрелов " + str(70) + "/70", 1 , (0, 255, 0))
            window.blit(a3, (20, 180))
        if kill >= 50:
            killscr = 0 
            a2 = font.render("- Убить 50 зомби " + str(50) + "/50", 1 , (0, 255, 0))
            window.blit(a2, (20, 150))
        if finish == True:
            window.blit(lose, (600, 350))
        if kill >= 50 and blast >= 70:
            a1 = font.render("Цель: ", 1 , (0, 255, 0))
            window.blit(a1, (20, 120))
            mixer.music.stop()
            winer.play()
            finish = True
            window.blit(win, (600, 350))