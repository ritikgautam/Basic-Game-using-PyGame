#importing pygame module
import pygame
from pygame.constants import HIDDEN

#initializing pygame
pygame.init()

#for display screen                w    h
window = pygame.display.set_mode((500,480))
pygame.display.set_caption("Ritik Game")

#making list of all images of Right-Move,Left-Move,Background Image and standing-position
walkRight = [pygame.image.load('Images\R1.png'), pygame.image.load('Images\R2.png'), pygame.image.load('Images\R3.png'), pygame.image.load('Images\R4.png'), pygame.image.load('Images\R5.png'), pygame.image.load('Images\R6.png'), pygame.image.load('Images\R7.png'), pygame.image.load('Images\R8.png'), pygame.image.load('Images\R9.png')]
walkLeft = [pygame.image.load('Images\L1.png'), pygame.image.load('Images\L2.png'), pygame.image.load('Images\L3.png'), pygame.image.load('Images\L4.png'), pygame.image.load('Images\L5.png'), pygame.image.load('Images\L6.png'), pygame.image.load('Images\L7.png'), pygame.image.load('Images\L8.png'), pygame.image.load('Images\L9.png')]
bg = pygame.image.load(r'C:\Users\dell\Desktop\python\Images\bg.jpg')
char = pygame.image.load('Images\standing.png')


#clock speed
clock = pygame.time.Clock()

#Load Suond Effects
bulletSound = pygame.mixer.Sound(r'C:\Users\dell\Desktop\python\Images\bullet.wav')
hitSound = pygame.mixer.Sound('Images\hit.wav')
jumpSound = pygame.mixer.Sound('Images\jump.wav')
gameoverSound = pygame.mixer.Sound('Images\gameover.wav')


music = pygame.mixer.music.load('Images\music.mp3')
pygame.mixer.music.play(-1)     #-1 ensures that if music ends, it continues to play again from start

screenWidth = 500
screenHeight = 500

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x                       # 2 object dimentions # x-coordinate
        self.y = y                        #y-coordinate
        self.width = width
        self.height = height
        self.vel = 5                 #velocity
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y+11, 29, 52)       #its a rectangle with coordinates

    def drawPlayer(self):
        if self.walkCount+1>=27:
            self.walkCount=0
        #drawing character in game
        
        if not(self.standing):
            if self.left:
                window.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                window.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:
            if self.right:
                window.blit(walkRight[0],(self.x,self.y))
            else:
                window.blit(walkLeft[0],(self.x,self.y))
        self.hitbox = (self.x + 17, self.y+11, 29, 52) 
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        window.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:                       #time delay for the text to remain for some time on screen
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit()
        pygame.mixer.music.play(-1)


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)
        



class enemy(object):
    walkRight = [pygame.image.load('Images\R1E.png'), pygame.image.load('Images\R2E.png'), pygame.image.load('Images\R3E.png'), pygame.image.load('Images\R4E.png'), pygame.image.load('Images\R5E.png'), pygame.image.load('Images\R6E.png'), pygame.image.load('Images\R7E.png'), pygame.image.load('Images\R8E.png'), pygame.image.load('Images\R9E.png'), pygame.image.load('Images\R10E.png'), pygame.image.load('Images\R11E.png')]
    walkLeft = [pygame.image.load('Images\L1E.png'), pygame.image.load('Images\L2E.png'), pygame.image.load('Images\L3E.png'), pygame.image.load('Images\L4E.png'), pygame.image.load('Images\L5E.png'), pygame.image.load('Images\L6E.png'), pygame.image.load('Images\L7E.png'), pygame.image.load('Images\L8E.png'), pygame.image.load('Images\L9E.png'), pygame.image.load('Images\L10E.png'), pygame.image.load('Images\L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x                   
        self.y = y                        
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x,self.end]
        self.vel = 3  
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self):
        self.move()
        if self.visible:
            if self.walkCount + 1 >=33:
                self.walkCount = 0
            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                window.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            #Drawing Health Bars
            pygame.draw.rect(window,(255,0,0),(self.hitbox[0],self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(window,(0,128,0),(self.hitbox[0],self.hitbox[1]-20, 5*(self.health), 10))
            #updating hitbox
            self.hitbox = (self.x + 17, self.y+2, 31, 57)
        # pygame.draw.rect(window,(255,0,0),self.hitbox,2)

        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel <self.path[1]:
                self.x+=self.vel
            else:
                self.vel = self.vel* -1
                self.walkCount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel* -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health-=1
        else:
            self.visible = False
        print('Hit')



#Draw on screen
def redrawGameWindow():
    #fill the screen before creating new rectangle
    #now fix the background image
    window.blit(bg,(0,0))

    #render text 
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    window.blit(text, (390,10))

    noobie.drawPlayer()
    
    #for bullets
    for bullet in bullets:
        bullet.draw()

    #for enemies
    goblin.draw()
    #refreshing
    pygame.display.update()






#mainloop
#function for font          type       size  Bold  Italic
font = pygame.font.SysFont('comicsans', 30,  True, False)
noobie = player(300,410,64,64)
goblin = enemy(100,410,64,64,450)
shootLoop = 0
bullets = []
run = True
while run:
    #pygame.time.delay(40)   #time in miliseconds #40fps
    clock.tick(27)           #fps

    #checking for collision between noobie and goblin
    if goblin.visible:
        if noobie.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and noobie.hitbox[1] + noobie.hitbox[3] > goblin.hitbox[1]:
                if noobie.hitbox[0] + noobie.hitbox[2] > goblin.hitbox[0] and noobie.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    pygame.mixer.music.stop()
                    gameoverSound.play()
                    noobie.hit()
                    score -=5

    if shootLoop > 0:
        shootLoop+=1
    if shootLoop > 3:
        shootLoop=0

    #events
    for event in pygame.event.get():
        #event for quit
        if event.type == pygame.QUIT:
            run = False
    
    #for bullets
    for bullet in bullets:
        #for collision
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1]+goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score +=1
                    bullets.pop(bullets.index(bullet))

        #for movement of bullets
        if bullet.x<screenWidth and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    #pressing keys
    #keys will be a list
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop==0: 
        bulletSound.play()
        if noobie.left:
            facing =-1
        else:
            facing =1
        if len(bullets)<5:
            bullets.append(projectile(round(noobie.x + noobie.width//2),round(noobie.y+noobie.height//2),6,(0,0,0),facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and noobie.x>noobie.vel:
        noobie.x-=noobie.vel
        noobie.left = True
        noobie.right = False
        noobie.standing = False
    elif keys[pygame.K_RIGHT] and noobie.x < screenWidth-noobie.width-noobie.vel:
        noobie.x+=noobie.vel
        noobie.left = False
        noobie.right = True
        noobie.standing=False
    else:
        noobie.standing = True
        noobie.walkCount = 0
    if not(noobie.isJump):
        if keys[pygame.K_UP]:
            jumpSound.play()
            noobie.isJump =  True
            noobie.standing = True
            noobie.walkCount = 0
    else:
        if noobie.jumpCount>=0:
            noobie.y-=(noobie.jumpCount**2)*0.5
            noobie.jumpCount-=1
        elif noobie.jumpCount>=-10:
            noobie.y+=(noobie.jumpCount**2)*0.5
            noobie.jumpCount-=1
        else:
            noobie.isJump = False
            noobie.jumpCount = 10
    redrawGameWindow()
    

pygame.quit()


