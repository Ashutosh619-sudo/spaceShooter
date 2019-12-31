import random
import pygame
import sys
from pygame.locals import *
import os



pygame.init()
screen_width = 600
screen_height = 604
Screen = pygame.display.set_mode((screen_width,screen_height))

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
     
background = pygame.image.load("data/backgrounds/starBackground.png").convert()
background1 = pygame.image.load("data/backgrounds/starBackground.png").convert()
bgy1 = -background.get_height()

bgx = 0
bgy = 0

def movingBackgorund():
    global bgx1,bgy1,bgy,bgx
    bgy += 5
    bgy1 += 5

    if bgy >= 604:
        bgy = -604
    if bgy1 >= 604:
        bgy1 = -604

    Screen.blit(background,(bgx,bgy))        
    Screen.blit(background1,(bgx,bgy1))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("playerSprites/player.png", -1)
        self.rect.center = (300,302)
        self.dx = 0
        self.dy = 0
        self.reset()
        self.lasertimer = 0
        self.lasermax = 5

    def update(self):
        self.rect.move_ip(self.dx,self.dy)
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.lasertimer = self.lasertimer + 1
            if self.lasertimer == self.lasermax:
                laserSprites.add(Laser(self.rect.midtop))
                self.lasertimer = 0       

        if self.rect.left < 0:
            self.rect.left = 0         
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height        

    def reset(self):
        self.rect.bottom = 600 

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("playerSprites/laserGreen.png",-1)
        self.rect.center = pos

    def update(self):
        if self.rect.top < 0:
            self.kill()    
        else:
            self.rect.move_ip(0,-15)
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("playerSprites/laserRed.png",-1)
        self.rect.center =pos
    
    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        else:
            self.rect.move_ip(0,15)    

class Enemy(pygame.sprite.Sprite):
    def __init__(self,centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemySprites/enemyShip.png",-1)
        self.dy = 8
        self.dx = -8
        self.reset()

    def update(self):   
        self.rect.centery += self.dy
        self.rect.centerx += self.dx
        if self.rect.bottom > Screen.get_height():
            self.reset()
        efire = random.randint(1,60)

        if efire == 1:
            enemyLaserSprites.add(EnemyLaser(self.rect.midbottom))

        if pygame.sprite.groupcollide(enemySprites,laserSprites,1,1):
            explosionSprites.add(EnemyExplosion(self.rect.center))
     

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, Screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)   

class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("playerSprites/laserGreenShot.png", -1)
        self.rect.center = pos        
        self.counter = 0
        self.maxcount = 10
    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()


def game():
    player= Player()
    playerSprite = pygame.sprite.RenderPlain((player))


    global laserSprites
    laserSprites = pygame.sprite.RenderPlain(())
    keepGoing = True
    global enemySprites
    enemySprites = pygame.sprite.RenderPlain(())
    enemySprites.add(Enemy(200))

    global enemyLaserSprites
    enemyLaserSprites = pygame.sprite.RenderPlain(())

    global explosionSprites
    explosionSprites = pygame.sprite.RenderPlain(())

    counter = 0
    clock = pygame.time.Clock()
    while keepGoing:
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == QUIT:
                    keepGoing = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
                    elif event.key == pygame.K_LEFT:
                        player.dx = -10
                    elif event.key == K_RIGHT:
                        player.dx = 10
                    elif event.key == K_UP:
                        player.dy = -10
                    elif event.key == K_DOWN:
                        player.dy = 10
                    elif event.type == K_SPACE:
                        laser.update()    
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        player.dx = 0
                    elif event.key == K_RIGHT:
                        player.dx = 0
                    elif event.key == K_UP:
                        player.dy = 0
                    elif event.key == K_DOWN:
                        player.dy = 0
                    

        movingBackgorund()              

        playerSprite.update()
        playerSprite.draw(Screen)
        laserSprites.update()
        laserSprites.draw(Screen)
        enemySprites.update()
        enemySprites.draw(Screen)
        enemyLaserSprites.update()
        enemyLaserSprites.draw(Screen)
        explosionSprites.update()
        explosionSprites.draw(Screen)
        clock.tick(30)

        counter += 1
        if counter >= 50:
            enemySprites.add(Enemy(300))
            counter = 0


        for hit in pygame.sprite.groupcollide(enemyLaserSprites,playerSprite,1,0):
            explosionSprites.add(EnemyExplosion(player.rect.center))
            playerSprite.remove(player)

        for hit in pygame.sprite.groupcollide(enemySprites,playerSprite,1,0):
            explosionSprites.add(EnemyExplosion(player.rect.center))
            playerSprite.remove(player)    
            
             
            
game()
