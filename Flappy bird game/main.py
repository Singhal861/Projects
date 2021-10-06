import random
import sys
import pygame
from pygame.locals import *
import time

 
FPS = 32
SCREENWIDTH =289
SCREENHEIGHT =511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES ={}
GAME_SOUNDS = {}
PLAYER = 'Gallery/Images/bird.png'
BACKGROUND = 'Gallery/Images/background.jpg'
PIPE = 'Gallery/Images/pipe.png'

def welcomeScreen():
    '''shows welcome image on the screen'''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENWIDTH*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                GAME_SOUNDS['die'].play()

                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # creat 2 pypes for blitting on the sreen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]
    pipeVelX = -4

    playerVelY = -9
    playerMaxVely = 10
    playeMinVely = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or (event.key == K_SPACE or event.key == K_UP):
                if playery > 0 :
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    # GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVely and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY- playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            lowerPipe['x'] += pipeVelX
            upperPipe['x'] += pipeVelX
            

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0< upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True


                
            



def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randint(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex =SCREENWIDTH +10
    y1 = pipeHeight - y2 + offset
    pipe = [
    {'x': pipex, 'y': -y1},
    {'x': pipex, 'y': y2}
    ]
    return pipe


if __name__ == '__main__':
    #this will be the main funct from where our game start
    pygame.init() #initialise all pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy game by Abhishek')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/Images/0.png').convert_alpha(),
        pygame.image.load('Gallery/Images/1.png').convert_alpha(),
        pygame.image.load('Gallery/Images/2.png').convert_alpha(),
        pygame.image.load('Gallery/Images/3.png').convert_alpha(),
        pygame.image.load('Gallery/Images/4.png').convert_alpha(),
        pygame.image.load('Gallery/Images/5.png').convert_alpha(),
        pygame.image.load('Gallery/Images/6.png').convert_alpha(),
        pygame.image.load('Gallery/Images/7.png').convert_alpha(),
        pygame.image.load('Gallery/Images/8.png').convert_alpha(),
        pygame.image.load('Gallery/Images/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('Gallery/Images/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/Images/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha())

    GAME_SOUNDS['die']= pygame.mixer.Sound('Gallery/Sound/die.mp3')
    GAME_SOUNDS['hit']= pygame.mixer.Sound('Gallery/Sound/hit.mp3')
    GAME_SOUNDS['point']= pygame.mixer.Sound('Gallery/Sound/point.mp3')
    GAME_SOUNDS['swoosh']= pygame.mixer.Sound('Gallery/Sound/Swoosh.mp3')
    GAME_SOUNDS['wing']= pygame.mixer.Sound('Gallery/Sound/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
