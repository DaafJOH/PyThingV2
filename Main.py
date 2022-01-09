import pygame, pickle, time

with open("Settings.txt", "rb") as settingsfile:
    try: settings = pickle.load(settingsfile)
    except EOFError: settings = {
        "Resolution":(1440, 800), # Resolution in (width, height)
        "Fullscreen":False, # if fullscreen is enabled
        "Server":0, # index in Servers
        "Servers":[{"Name":"Official", "Host":"127.0.0.1", "Port":65432}]} # list of servers

FPS = 60
VEL = 5
BULLET_VEL = 40
WIDTH, HEIGHT = 1280, 720
SCALE = WIDTH / settings["Resolution"][0], HEIGHT / settings["Resolution"][1]

pygame.init()
running = True
window = pygame.display.set_mode(settings["Resolution"])
display = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.display.set_caption("PyThing")

import Constants, Modules

# TODO Function for connecting with the server
def Connect():
    pass

# TODO Function for disconnecting with the server
def Disconnect():
    pass

# Function to scale the display correctly
def Display_Window(display, skip=False, absolute=False):
    width, height = settings["Resolution"]

    # If the aspact ratio is the same as original image
    if width / WIDTH == height / HEIGHT or absolute:
        frame = pygame.transform.scale(display, (width, height)) # Just scale the image to the new resolution
        window.blit(frame, (0, 0)) # Because of the same size it can stay at the same place

    # If the height is higher than normal
    elif width / WIDTH < height / HEIGHT:
        frame = pygame.transform.scale(display, (int(width * (height / HEIGHT)), height)) # TODO make proper commenting for this function
        window.blit(frame, (0 - (int(width * (height / HEIGHT)) - width) / 2, 0))

    # If the width is wider than normal
    elif width / WIDTH > height / HEIGHT:
        frame = pygame.transform.scale(display, (width, int(height * (width / WIDTH))))
        window.blit(frame, (0, 0 - (int(height * (width / WIDTH)) - height) / 2))
    if not skip: pygame.display.update()

def SliderAnimation(display, startingDisplay, endingDisplay, direction):
    position, speed = 0, 0
    while True:
        if direction == "Up" or direction == "Down":
            if position <= HEIGHT: speed += 1
            elif speed > 1:  speed -= 1
            if position+speed > HEIGHT: break
            else: position += speed
        elif direction == "Left" or direction == "Right":
            if position <= WIDTH: speed += 1
            elif speed > 1:  speed -= 1
            if position+speed > WIDTH: break
            else: position += speed
        
        if direction == "Up":
            display.blit(Constants.BACKGROUND, (0, position))
            display.blit(Constants.BACKGROUND, (0, position-HEIGHT))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (0, position))
            display.blit(endingDisplay, (0, position-HEIGHT)) 
        elif direction == "Left":
            display.blit(Constants.BACKGROUND, (position, 0))
            display.blit(Constants.BACKGROUND, (position-WIDTH, 0))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            #display.blit(startingDisplay, (position, 0))
            #display.blit(endingDisplay, (position-WIDTH, 0))
        elif direction == "Right":
            display.blit(Constants.BACKGROUND, (0-position, 0))
            display.blit(Constants.BACKGROUND, (0-position+WIDTH, 0))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (0-position, 0))
            display.blit(endingDisplay, (0-position+WIDTH, 0))
        elif direction == "Down":
            display.blit(Constants.BACKGROUND, (0, 0-position))
            display.blit(Constants.BACKGROUND, (0, 0-position+HEIGHT))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (0, 0-position))
            display.blit(endingDisplay, (0, 0-position+HEIGHT))
        Display_Window(display, absolute=True)
    display.blit(endingDisplay, (0, 0))
    Display_Window(display, absolute=True)

# TODO Main menu function
def GUI_Main():
    global running
    breaked = False
    menuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    LoadButton = Modules.Button(menuDisplay, (50, 125), (300, 100), "Load Game", SCALE)
    NewButton = Modules.Button(menuDisplay, (50, 275), (300, 100), "New Game", SCALE)
    ServerButton = Modules.Button(menuDisplay, (50, 425), (300, 100), "Select Server", SCALE)
    SettingsButton = Modules.Button(menuDisplay, (50, 575), (300, 100), "Settings", SCALE)

    while running and not breaked:
        menuDisplay.fill((0, 0, 0))
        menuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(menuDisplay, skip=True)
        
        menuDisplay.fill((0, 0, 0, 0))
        LoadButton.Update()
        NewButton.Update()
        ServerButton.Update()
        SettingsButton.Update()
        
        Display_Window(menuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if LoadButton.over:
                    if GUI_Load(menuDisplay): breaked = True
                elif NewButton.over:
                    if GUI_New(menuDisplay): breaked = True

        clock.tick(FPS)

# TODO Load game menu function
def GUI_Load(menuDisplay):
    global running
    breaked = False
    LmenuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    LmenuDisplay.fill((0, 0, 0, 0))
    Save1Button = Modules.Button(LmenuDisplay, (50, 50), (300, 100), "Load Save", SCALE)
    Save1Button.Update()

    SliderAnimation(display, menuDisplay, LmenuDisplay, "Up")

    while running and not breaked:
        LmenuDisplay.fill((0, 0, 0))
        LmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(LmenuDisplay, skip=True)

        LmenuDisplay.fill((0, 0, 0, 0))
        Save1Button.Update()
        Display_Window(LmenuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SliderAnimation(display, LmenuDisplay, menuDisplay, "Down")
                    breaked = True
                    break

# TODO New game menu function
def GUI_New(menuDisplay):
    global running
    breaked = False
    NmenuDisplay = pygame.Surface(settings["Resolution"])
    NmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
    Save1Button = Modules.Button(NmenuDisplay, (50, 50), (300, 100), "New Save", SCALE)
    Save1Button.Update()

    SliderAnimation(display, menuDisplay, NmenuDisplay, "Left")

    while running and not breaked:
        NmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Save1Button.Update()
        display.blit(NmenuDisplay, (0, 0))
        Display_Window(display, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SliderAnimation(display, NmenuDisplay, menuDisplay, "Right")
                    breaked = True
                    break

# TODO Server select menu function
def GUI_Server():
    pass

# TODO Options menu function
def GUI_Options():
    pass

# TODO Ingame pause menu function
def IGGUI_Pause():
    pass

# TODO Main game loop
def Main():
    GUI_Main()

Main()

pygame.quit()