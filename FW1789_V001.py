import pygame
from pygame.locals import *
import sys, os, random, time, math
import json

# local imports
import FW1789_VG as VG
from FW1789_stages import *
from FW1789_sounds import *
from FW1789_caravan import caravan
from FW1789_threat import threat

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


try:
    import pygame
    from pygame.locals import *
    import sys, os, random, time, math
    import json
    
    # local imports
    import FW1789_VG as VG
    from FW1789_stages import *
    from FW1789_sounds import *
    from FW1789_caravan import caravan
    from FW1789_threat import threat

except ImportError as e:
    print(f"ERROR IMPORTING MODULES: {e}")
    raise SystemExit(f"ERROR IMPORTING MODULES: {e}")

global hiscore
hiscore = 20 # time to stage die
try:
    with open("hiscore.json", "rt") as infile:
        hiscore = json.load(infile)
except:
    print("WARNING: unable to load HiScore")

pygame.init()

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption(f"FW1789 - v{VG.FW1789_version}")
icone = pygame.image.load("Images/icone2b.png").convert_alpha()
pygame.display.set_icon(icone)
pygame.mouse.set_visible(False)

lettre = pygame.font.Font("freesansbold.ttf", 30)
FWlettre = pygame.font.Font("fonts_western/RioGrande2.ttf", 28)

explode1 = pygame.image.load("Images/explosion1.png").convert_alpha()       
explode2 = pygame.image.load("Images/explosion2.png").convert_alpha()       
explode3 = pygame.image.load("Images/explosion3.png").convert_alpha()       
explode4 = pygame.image.load("Images/explosion4.png").convert_alpha()       
explode5 = pygame.image.load("Images/explosion5.png").convert_alpha()       
explode6 = pygame.image.load("Images/explosion6.png").convert_alpha()       

class mire(pygame.sprite.Sprite):
    def __init__(self, image, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"Images/{image}")
        self.rect = self.image.get_rect()
        self.rect.x = 800 / 2
        self.rect.y = 600 / 2

        self.grenades = VG.ParGrenadeQty # 10
        self.bullets = VG.ParBulletQty # 30
        self.life = VG.ParLife # 100
        self.score = 0

    def move(self):
        mousepos = pygame.mouse.get_pos()
        self.rect.x = mousepos[0] 
        self.rect.y = mousepos[1]
        fenetre.blit(self.image, self.rect)

    def shoot(self):
        if self.bullets > 0:
            self.bullets -= 1
            S_Shoot.play()

            yeah = pygame.sprite.spritecollide(self, groupBandits, dokill=False)
            if yeah:
                for bandi in yeah:
                    bandi.shooted(10)
                    self.score += 10
                    if bandi.life > 0:
                        S_Rire.play()
                    else:
                        S_Argh.play()
                        groupBandits.remove(bandi)

            yeah = pygame.sprite.spritecollide(self, groupBonusGrenades, dokill=True)
            if yeah:
                for idx, tt in enumerate(yeah):
                    if yeah[idx].life > 0:
                        yeah[idx].shooted(1000)
                        self.grenades += 5
                        S_Yeah.play()

            yeah = pygame.sprite.spritecollide(self, groupBonusBullets, dokill=True)
            if yeah:
                for idx, tt in enumerate(yeah):
                    if yeah[idx].life > 0:
                        yeah[idx].shooted(1000)
                        self.bullets += 10
                        S_Yeah.play()

            HoNo = pygame.sprite.spritecollide(self, groupFarmers, dokill=False)
            if HoNo:
                self.life -= 10
                S_Argh.play()
                return "Loser"
            else:
                return "Ouf"

    def getxy(self):
        return (self.rect.x, self.rect.y)

class grenade(pygame.sprite.Sprite):
    def __init__(self, image, owner):
        pygame.sprite.Sprite.__init__(self)
        self.time = 30
        self.image = pygame.image.load(f"Images/{image}")
        self.rect = self.image.get_rect()
        self.imageOri = pygame.image.load(f"Images/{image}")
        self.rectOri = self.imageOri.get_rect()

        self.launched = False
        self.owner = owner # 1,2,3,4 to know who player got this grenade

        self.rect.x = 30 # initial position
        self.rect.y = 550
        self.newrect = self.image.get_rect()
        self.newrect.x = mire1.getxy()[0] # final position
        self.newrect.y = 550
        self.movx = (self.newrect.x - self.rect.x) / self.time
        self.movy = (self.newrect.y - self.rect.y) / self.time
        self.counter = int(self.time)

        if self.newrect.x > self.rect.x:
            self.elipse_fwrw = True
            self.elipse_rayon = int((self.newrect.x - self.rect.x) / 2)
            self.elipse_center = self.rect.x + self.elipse_rayon
            self.angle = 0
        else:
            self.elipse_fwrw = False
            self.elipse_rayon = int((self.rect.x - self.newrect.x) / 2)
            self.elipse_center = self.newrect.x + self.elipse_rayon
            self.angle = math.pi

    def launch(self):
        self.newrect.x = mire1.getxy()[0]
        self.newrect.y = 550

        if mire1.getxy()[0] > 400:
            self.rect.x = 760
        else:
            self.rect.x = 0
        self.rect.y = 550

        self.newrect = self.image.get_rect()
        self.newrect.x = mire1.getxy()[0] + 25 # final position [mireWidth-grenadeWidth]
        self.newrect.y = 550
        self.movx = (self.newrect.x - self.rect.x) / self.time
        self.movy = (self.newrect.y - self.rect.y) / self.time
        self.counter = 0

        if self.newrect.x > self.rect.x:
            self.elipse_fwrw = True
            self.elipse_rayon = int((self.newrect.x - self.rect.x) / 2)
            self.elipse_center = self.rect.x + self.elipse_rayon
            self.angle = 0
        else:
            self.elipse_fwrw = False
            self.elipse_rayon = int((self.rect.x - self.newrect.x) / 2)
            self.elipse_center = self.newrect.x + self.elipse_rayon
            self.angle = math.pi

        self.launched = True

    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(image, angle)
        w = math.sqrt(rect.width**2 + rect.height**2)
        self.rect = self.image.get_rect(center=rect.center, size=(w, w))
        
def moveElipse(self):
    if self.angle > math.pi or self.angle < 0:
            # Some more delay to explode
        self.counter += 1
        if self.counter >= 30:
            fenetre.blit(explode4, (self.rect[0] - 30, 500))
        if 20 <= self.counter < 30:
            fenetre.blit(explode3, (self.rect[0] - 30, 500))
        if 10 <= self.counter < 20:
            fenetre.blit(explode2, (self.rect[0] - 30, 500))
            # Delay to check if shoot caravan
        if self.counter < 10:
            fenetre.blit(explode1, (self.rect[0] - 30, 500))

            yeah = pygame.sprite.spritecollide(self, groupCaravans, dokill=True)
            for idx, cara in enumerate(yeah):
                yeah[idx].life = 0
                mire1.score += 100
                S_Bomb.play()  # caravan shooted
                S_Bomb1.stop()
                self.counter = 10  # pass to big explosion animation

            if self.counter == 9:
                S_Bomb1.play()  # caravan not shooted
                self.launched = False

        if self.counter > 40:
            self.launched = False
    else:
        if self.elipse_fwrw:
            self.angle += VG.ParGrenadeSpeed  # 0.03
        else:
            self.angle -= VG.ParGrenadeSpeed  # 0.03

        self.rot_center(self.imageOri, self.rectOri, math.degrees(float(self.angle * 2)))

        self.movx = math.cos(self.angle) * self.elipse_rayon
        self.movy = math.sin(self.angle) * 550

        if self.elipse_fwrw:
            self.rect.x = self.elipse_center - self.movx
            self.rect.y = 550 - self.movy
        else:
            self.rect.x = self.elipse_center - self.movx
            self.rect.y = 550 - self.movy

        fenetre.blit(self.image, self.rect)

    return self.launched
def getxy(self):
	return self.rect.x, self.rect.y

def getangle(self):
	return self.angle

def getfwrw(self):
	return self.elipse_fwrw

def wait_mouse_click():
    """Wait for 0.5 second, then mouse click, and 0.2 second"""
    time.sleep(0.5)  # minimum time
    for event in pygame.event.get():  # purge pygame event queue
        pass
    wait_mouse_click = True
    is_running = True
    while wait_mouse_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                wait_mouse_click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                    wait_mouse_click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                wait_mouse_click = False
    time.sleep(0.2)  # minimum time

def save_hiscore(score):
    """Save HiScore if new record"""
    global hiscore
    if hiscore < score:
        hiscore = score
        try:
            with open('hiscore.json', 'w') as outfile:
                json.dump(hiscore, outfile)
        except:
            print("WARNING: unable to write HiScore")

def blit_scores():
    """Finally blit scores for all players"""
    fenetre.blit(FWlettre.render(f"Remaining Time: {timeLeft // 10}.{timeLeft % 10}", True, (255, 0, 0)), (5, 5))
    fenetre.blit(FWlettre.render(f"HiScore: {hiscore}", True, (255, 0, 0)), (5, 30))
    fenetre.blit(FWlettre.render(f"Stage: {StageNumber + 1}", True, (255, 0, 0)), (5, 55))
    fenetre.blit(FWlettre.render(f"Life: {mire1.life}", True, (255, 0, 0)), (600, 5))
    fenetre.blit(FWlettre.render(f"Bullets: {mire1.bullets}", True, (255, 0, 0)), (600, 30))
    fenetre.blit(FWlettre.render(f"Grenades: {mire1.grenades}", True, (255, 0, 0)), (600, 55))
    fenetre.blit(FWlettre.render(f"Score: {mire1.score}", True, (255, 0, 0)), (600, 80))

def gameOver():
    wait_mouse_click()
    save_hiscore(mire1.score)
    
    listGrenades = []
    gameTerminate = False
    crono = pygame.time.Clock()
    milli = 0
    VG.last5sec = 5

    StageNumber = 0
    StageTerminate = False
    fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
    fondomusic.play()
#################################################
def loadStageSprites(StageNumber):
	groupBandits = pygame.sprite.Group()
	for idx in range(StagesBandits[StageNumber][0]):
		varRand = random.randrange(0, 3)
		if varRand == 0:
			bandit1 = threat("Dalton-Williamb.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		elif varRand == 1:
			bandit1 = threat("bandit2b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		elif varRand >= 2:
			bandit1 = threat("bandit4b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		groupBandits.add(bandit1)

	groupFarmers = pygame.sprite.Group()
	for idx in range(StagesFarmers[StageNumber][0]):
		varRand = random.randrange(0, 2)
		if varRand == 0:
			farmer1 = threat("farmerb.png", StagesFarmers[StageNumber][1], 1) #image, speed, life
		elif varRand >= 1:
			farmer1 = threat("Dalton-Ma-b.png", StagesFarmers[StageNumber][1], 1) #image, speed, life
		groupFarmers.add(farmer1)

	listCaravans = []
	groupCaravans =  pygame.sprite.Group()
	for idx in range(StagesDiligences[StageNumber][0]):
		varRand = random.randrange(0, 4)
		if varRand == 0:
			caravan1 = caravan("caravan4a.png", 90)
		elif varRand == 1:
			caravan1 = caravan("caravan2b.png", 90)
		elif varRand == 2:
			caravan1 = caravan("caravan1c.png", 90)
		elif varRand >= 3:
			caravan1 = caravan("caravan3b.png", StagesDiligences[StageNumber][1]) #image, speed
		
		listCaravans.append(caravan1)
		groupCaravans.add(caravan1)

	# add grenades bonus for diligences to hit
	groupBonusGrenades = pygame.sprite.Group()
	for idx in range(StagesGrenades[StageNumber][0]):
		bonus1 = threat("Grenade-6b.png", StagesGrenades[StageNumber][1], 1) #image, speed, life
		groupBonusGrenades.add(bonus1)

	# add as bullets bonus 
	groupBonusBullets = pygame.sprite.Group()
	for idx in range(StagesBullets[StageNumber][0]):
		#bonus1 = threat("bullets-2b.png", StagesBullets[StageNumber][1], 1) #image, speed, life
		bonus1 = threat("bullets-b.png", StagesBullets[StageNumber][1], 1) #image, speed, life
		groupBonusBullets.add(bonus1)
		
	return groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets

#################################################
def loadStageSprites(StageNumber):
    groupBandits = pygame.sprite.Group()
    for _ in range(StagesBandits[StageNumber][0]):
        varRand = random.randrange(0, 3)
        if varRand == 0:
            bandit1 = threat("Dalton-Williamb.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
        elif varRand == 1:
            bandit1 = threat("bandit2b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
        else:
            bandit1 = threat("bandit4b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
        groupBandits.add(bandit1)

    groupFarmers = pygame.sprite.Group()
    for _ in range(StagesFarmers[StageNumber][0]):
        varRand = random.randrange(0, 2)
        if varRand == 0:
            farmer1 = threat("farmerb.png", StagesFarmers[StageNumber][1], 1)
        else:
            farmer1 = threat("Dalton-Ma-b.png", StagesFarmers[StageNumber][1], 1)
        groupFarmers.add(farmer1)

    listCaravans = []
    groupCaravans = pygame.sprite.Group()
    for _ in range(StagesDiligences[StageNumber][0]):
        varRand = random.randrange(0, 4)
        if varRand == 0:
            caravan1 = caravan("caravan4a.png", 90)
        elif varRand == 1:
            caravan1 = caravan("caravan2b.png", 90)
        elif varRand == 2:
            caravan1 = caravan("caravan1c.png", 90)
        else:
            caravan1 = caravan("caravan3b.png", StagesDiligences[StageNumber][1])

        listCaravans.append(caravan1)
        groupCaravans.add(caravan1)

    groupBonusGrenades = pygame.sprite.Group()
    for _ in range(StagesGrenades[StageNumber][0]):
        bonus1 = threat("Grenade-6b.png", StagesGrenades[StageNumber][1], 1)
        groupBonusGrenades.add(bonus1)

    groupBonusBullets = pygame.sprite.Group()
    for _ in range(StagesBullets[StageNumber][0]):
        bonus1 = threat("bullets-b.png", StagesBullets[StageNumber][1], 1)
        groupBonusBullets.add(bonus1)

    return groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets

def loadStageEnv(StageNumber):
    fondo1 = pygame.image.load(f"background/{StagesBckGnd1[StageNumber]}.jpg")
    fondo2 = pygame.image.load(f"background/{StagesBckGnd2[StageNumber]}.png")
    if fondo2.get_alpha() is None:
        fondo2 = fondo2.convert()
    else:
        fondo2 = fondo2.convert_alpha()

    fondomusic = pygame.mixer.Sound(f"Sounds/{StagesMusic[StageNumber]}.ogg")
    pygame.mixer.stop()
    return fondo1, fondo2, fondomusic

BckGndWin = pygame.image.load("background/festival-far-westa.jpg")
BckGndLoseTime = pygame.image.load("background/western-jail.jpg")
BckGndLoseLife = pygame.image.load("background/pendu-meridien-de-sang.jpg")

pygame.mixer.init()
pygame.mixer.music.set_volume(VG.ParMusicVol)

S_Menu.play()

background = pygame.image.load("background/FarWest1789b.jpg")
fenetre.blit(background, (0, 0))
pygame.display.update()
wait_mouse_click()

mire1 = mire("mire-red.png", 1)
listMire = pygame.sprite.Group()
listMire.add(mire1)

grenadeBlue = grenade("grenade-blue.png", 1)
grenadeRed = grenade("grenade-red.png", 2)
grenadeGreen = grenade("grenade-green.png", 3)
grenadeYellow = grenade("grenade-yellow.png", 4)
listGrenades = []
groupGrenades = pygame.sprite.Group()
listGrenades.append(grenadeBlue)
groupGrenades.add(grenadeBlue)

crono = pygame.time.Clock()
milli = 0

StageNumber = 0
StageTerminate = False

groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
fondomusic.play()

gameTerminate = False

scroll1 = 0
scroll2 = 0

VG.last5sec = 5

if VG.ParGrabMouse:
    pygame.event.set_grab(True)

is_running = True
while is_running:
    milli += crono.tick()
    timeLeft = StagesTime[StageNumber] - milli // 100

    if timeLeft % 10 == 0:
        if int(timeLeft) in [40, 30, 20, 10]:
            if VG.last5sec == (int(timeLeft) // 10):
                S_Beep1.stop()
                S_Beep1.play()
                VG.last5sec -= 1

    if timeLeft < 1:
        gameTerminate = True

    scroll1 = (scroll1 + 1) % (800 * 2)
    scroll2 = (scroll2 + 2) % (800 * 2)

    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            is_running = False
        if action.type == pygame.KEYDOWN:
            if action.key == pygame.K_ESCAPE:
                is_running = False
        if action.type == pygame.MOUSEBUTTONDOWN:
            if action.button == 3:
                if mire1.grenades > 0:
                    grenadeBlue = grenade("grenade-blue.png", 1)
                    listGrenades.append(grenadeBlue)
                    listGrenades[-1].launch()
                    mire1.grenades -= 1
            if action.button == 1:
                shot = mire1.shoot()
                if shot == "Loser" and mire1.life <= 0:
                    gameTerminate = True

    if not gameTerminate:
        mousepos = pygame.mouse.get_pos()

        fenetre.blit(fondo1, (-800 * 2 + scroll1, 0))
        blit_scores()

        groupCaravans.update()
        groupCaravans.draw(fenetre)

        fenetre.blit(fondo2, (-800 * 2 + scroll2, 600 - mousepos[1]))

        for gren in listGrenades:
            if gren.launched:
                gren.moveEllipse()
                if not gren.getfwrw() and gren.getangle() <= math.pi / 2:
                    fenetre.blit(fondo2, (-800 * 2 + scroll2, 600 - mousepos[1]))
                if gren.getfwrw() and gren.getangle() > math.pi / 2:
                    fenetre.blit(fondo2, (-800 * 2 + scroll2, 600 - mousepos[1]))
            else:
                listGrenades.remove(gren)

        groupBandits.update()
        groupBandits.draw(fenetre)

        groupFarmers.update()
        groupFarmers.draw(fenetre)

        groupBonusGrenades.update()
        groupBonusGrenades.draw(fenetre)

        groupBonusBullets.update()
        groupBonusBullets.draw(fenetre)

        mire1.move()

        if not groupBandits:
            fenetre.blit(BckGndWin, (0, 0))
            if StageNumber < 9:
                StageNumber += 1
            blit_scores()
            S_Applause.play()

            mire1.score += timeLeft
            msg1 = FWlettre.render(f"SCORE TIME BONUS: +{timeLeft}", True, (255, 0, 0))
            msg2 = FWlettre.render("NEXT STAGE:", True, (255, 0, 0))
            msg3 = FWlettre.render(StagesMsg[StageNumber], True, (255, 0, 0))

            msg1pos = msg1.get_rect(centerx=fenetre.get_rect().centerx, centery=fenetre.get_rect().centery - 25)
            msg2pos = msg2.get_rect(centerx=fenetre.get_rect().centerx, centery=fenetre.get_rect().centery + 25)
            msg3pos = msg3.get_rect(centerx=fenetre.get_rect().centerx, centery=fenetre.get_rect().centery + 50)

            fenetre.blit(msg1, msg1pos)
            fenetre.blit(msg2, msg2pos)
            fenetre.blit(msg3, msg3pos)

            pygame.display.update()
            gameOver()

            mire1.bullets += 10  # bonus stage win
            listGrenades = []

            fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
            fondomusic.play()
            groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

            gameTerminate = False
            crono = pygame.time.Clock()
            milli = 0
    else:
        if timeLeft > 0:
            fenetre.blit(BckGndLoseLife, (0, 0))
            msg1 = FWlettre.render("YOU LOSE BY LIFE", True, (255, 0, 0))
        else:
            fenetre.blit(BckGndLoseTime, (0, 0))
            msg1 = FWlettre.render("YOU LOSE BY TIME", True, (255, 0, 0))

        msg1pos = msg1.get_rect(centerx=fenetre.get_rect().centerx, centery=fenetre.get_rect().centery - 25)
        fenetre.blit(msg1, msg1pos)

        blit_scores()
        pygame.display.update()

        S_Rire.play()
        gameOver()

        StageNumber = 0
        fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
        fondomusic.play()
        groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

        mire1.grenades = VG.ParGrenadeQty
        mire1.bullets = VG.ParBulletQty
        mire1.life = VG.ParLife
        mire1.score = 0
        listGrenades = []
        gameTerminate = False
        crono = pygame.time.Clock()
        milli = 0

    pygame.time.delay(10)
    pygame.display.flip()

pygame.quit()
sys.exit(0)
