import random, sys, time, pygame
FPS=90
width = 640
height = 480
flashspeed= 500 # in milliseconds
flash_delay= 200 
buttonsize = 200
buttongapsize = 20
timeout = 4 # seconds before game over if no button is pushed.

white = (255, 255, 255)
black  = (0, 0, 0)
bright_red  = (255, 0, 0)
red  = (155, 0, 0)
bright_green  = ( 0,255, 0)
green   = (0, 155, 0)
bright_blue = (0,0, 255)
blue = (0,0,155)
bright_yellow = (255, 255, 0)
yellow  = (155, 155, 0)
darkgray = ( 40, 40, 40)


x_margin = int((width - (2 * buttonsize) - buttongapsize) / 2)
y_margin= int((height - (2 * buttonsize) - buttongapsize) / 2)

# Rect objects for each of the four buttons
yellow_rect = pygame.Rect(x_margin, y_margin, buttonsize, buttonsize)
blue_rect   = pygame.Rect(x_margin + buttonsize+  buttongapsize, y_margin, buttonsize,buttonsize)
red_rect   = pygame.Rect(x_margin, y_margin+ buttonsize + buttongapsize,buttonsize, buttonsize)
green_rect = pygame.Rect(x_margin+ buttonsize +  buttongapsize, y_margin + buttonsize + buttongapsize,buttonsize,buttonsize)

def main():
    global clock,display_surf,basic_font

    pygame.init()
    clock=pygame.time.Clock()
    display_surf = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simulate')

    basic_font = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = basic_font.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, darkgray)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, height - 25)


    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True: 
        clickedButton = None # button that was clicked (set to yellow, red, green, or blue)
        display_surf.fill(black)
        drawButtons()

        scoreSurf = basic_font.render('Score: ' + str(score), 1, white)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (width - 100, 10)
        display_surf.blit(scoreSurf, scoreRect)

        display_surf.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = yellow
                elif event.key == K_w:
                    clickedButton = blue
                elif event.key == K_a:
                    clickedButton = red
                elif event.key == K_s:
                    clickedButton = green



        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((yellow, blue, red, green)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(flash_delay)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  
        terminate() 
    for event in pygame.event.get(KEYUP): 
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event) 


def flashButtonAnimation(color, animationSpeed=50):
    if color == yellow:
        flashColor = bright_yellow
        rectangle = yellow_rect
    elif color == blue:
        flashColor = bright_blue
        rectangle = blue_rect
    elif color == red:
        flashColor = bright_red
        rectangle = red_rect
    elif color == green:
        flashColor = bright_green
        rectangle = green_rect

    origSurf = display_surf.copy()
    flashSurf = pygame.Surface((buttonsize,buttonsize))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    for start, end, step in ((0, 255, 1), (255, 0, -1)): 
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            display_surf.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            display_surf.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            clock.tick(FPS)
    display_surf.blit(origSurf, (0, 0))


def drawButtons():
    pygame.draw.rect(display_surf, yellow, yellow_rect)
    pygame.draw.rect(display_surf, blue, blue_rect)
    pygame.draw.rect(display_surf,red, red_rect)
    pygame.draw.rect(display_surf,green,green_rect)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((width, height))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        display_surf.fill(black)

        newBgSurf.fill((r, g, b, alpha))
        display_surf.blit(newBgSurf, (0, 0))

        drawButtons() # redraw the buttons on top of the tint

        pygame.display.update()
        clock.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=white, animationSpeed=50):
    origSurf = display_surf.copy()
    flashSurf = pygame.Surface(display_surf.get_size())
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color
    for i in range(3): 
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step):              
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                display_surf.blit(origSurf, (0, 0))
                display_surf.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()  
                clock.tick(FPS)



def getButtonClicked(x, y):
    if yelllow_rect.collidepoint( (x, y) ):
        return yellow
    elif blue_rect.collidepoint( (x, y) ):
        return blue
    elif red_rect.collidepoint( (x, y) ):
        return red
    elif green_rect.collidepoint( (x, y) ):
        return green
    return None


if __name__ == '__main__':
    main()
