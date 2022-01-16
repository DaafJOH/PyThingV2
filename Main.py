import pygame, pickle, time, os, socket, threading

with open("Settings.txt", "rb") as settingsfile: # Open Settings file
    try: settings = pickle.load(settingsfile)
    except EOFError: settings = {
        "Resolution":(1280, 720), # Resolution in (width, height)
        "Fullscreen":False, # if fullscreen is enabled
        "Server":0, # index in Servers
        "Servers":[{"Name":"Official", "Host":"127.0.0.1", "Port":65432}]} # list of servers

FPS = 60 # Frames per second (com'on you know this)
VEL = 5 # Player velocety
BULLET_VEL = 40 # Bullet velocety
WIDTH, HEIGHT = 1280, 720 # Original screen resolution
SCALE = WIDTH / settings["Resolution"][0], HEIGHT / settings["Resolution"][1]
NAME, IP, PORT = settings["Servers"][settings["Server"]].values()
SOCKETS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKETS.connect((IP, PORT))

pygame.init()
running = True
window = pygame.display.set_mode(settings["Resolution"])
display = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.display.set_caption("PyThing")

import Constants

class Button:
    def __init__(self, display, position, size, text, side):
        self.DISPLAY = display # Display to use
        self.X, self.Y = position # Position at north-west
        self.WIDTH, self.HEIGHT = size # Size in pixels
        self.TEXT = text # Text to display
        self.SIDE = side # Side that the button won't expand

        self.over = False # True if mouse is over button
        self.scale = 1 # Scale factor when mouse is over button

        self.rect = pygame.Rect(position, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((100, 100, 100, 200))
        self.textImage = Constants.FONT.render(self.TEXT, 0, (0, 0, 0))

    def Update(self):
        if self.SIDE == "Left":
            self.rect.width, self.rect.height = int(self.WIDTH * self.scale), int(self.HEIGHT * self.scale)
            self.relHeight = self.Y - (self.rect.height - self.HEIGHT) / 2
            self.rect.y = self.relHeight
            self.DISPLAY.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.X, self.relHeight))
            self.StextImage = pygame.transform.scale(self.textImage, (int(self.textImage.get_width() * self.scale), int(self.textImage.get_height() * self.scale)))
            self.DISPLAY.blit(self.StextImage, self.StextImage.get_rect(center=(self.X + self.rect.width / 2, self.relHeight + self.rect.height / 2)))
            pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5)
            mousepos = pygame.mouse.get_pos()
            if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))):
                if self.scale < 1.5: self.scale += 0.1; self.over = True
            else:
                if self.scale > 1: self.scale -= 0.1; self.over = False
        elif self.SIDE == "Right":
            self.rect.width, self.rect.height = int(self.WIDTH * self.scale), int(self.HEIGHT * self.scale)
            self.relHeight = self.Y - (self.rect.height - self.HEIGHT) / 2
            self.rect.y = self.relHeight
            self.DISPLAY.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.X - (self.rect.width - self.WIDTH), self.relHeight))
            self.StextImage = pygame.transform.scale(self.textImage, (int(self.textImage.get_width() * self.scale), int(self.textImage.get_height() * self.scale)))
            self.DISPLAY.blit(self.StextImage, self.StextImage.get_rect(center=((self.X + self.rect.width / 2) - (self.rect.width - self.WIDTH), self.relHeight + self.rect.height / 2)))
            self.rect.x = self.X - (self.rect.width - self.WIDTH)
            pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5)
            mousepos = pygame.mouse.get_pos()
            if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))):
                if self.scale < 1.5: self.scale += 0.1; self.over = True
            else:
                if self.scale > 1: self.scale -= 0.1; self.over = False
        else:
            self.DISPLAY.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.X, self.Y))
            self.DISPLAY.blit(self.textImage, self.textImage.get_rect(center=(self.X + self.rect.width / 2, self.Y + self.rect.height / 2)))
            pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5)
            mousepos = pygame.mouse.get_pos()
            if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))):
                self.over = True
            else:
                self.over = False

    def UpdateText(self, text):
        self.TEXT = text
        self.textImage = Constants.FONT.render(self.TEXT, 0, (0, 0, 0))

# TODO Function for connecting with the server
def Connect():
    SOCKETS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKETS.connect((IP, PORT))

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
            if position <= HEIGHT/2: speed += 1
            elif speed > 1:  speed -= 1
            if position+speed > HEIGHT: break
            else: position += speed
        elif direction == "Left" or direction == "Right":
            if position <= WIDTH/2: speed += 1
            elif speed > 1:  speed -= 1
            if position+speed > WIDTH: break
            else: position += speed
        if direction == "Up":
            display.blit(Constants.BACKGROUND, (0, position/2))
            display.blit(Constants.BACKGROUND, (0, position/2-HEIGHT))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (0, position))
            display.blit(endingDisplay, (0, position-HEIGHT)) 
        elif direction == "Left":
            display.blit(Constants.BACKGROUND, (position/2, 0))
            display.blit(Constants.BACKGROUND, (position/2-WIDTH, 0))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (position, 0))
            display.blit(endingDisplay, (position-WIDTH, 0))
        elif direction == "Right":
            display.blit(Constants.BACKGROUND, (0-position/2, 0))
            display.blit(Constants.BACKGROUND, (0-position/2+WIDTH, 0))
            Display_Window(display, skip=True)
            display.fill((0, 0, 0, 0))
            display.blit(startingDisplay, (0-position, 0))
            display.blit(endingDisplay, (0-position+WIDTH, 0))
        elif direction == "Down":
            display.blit(Constants.BACKGROUND, (0, 0-position/2))
            display.blit(Constants.BACKGROUND, (0, 0-position/2+HEIGHT))
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
    LoadButton = Button(menuDisplay, (50, 125), (300, 100), "Load Game", "Left")
    NewButton = Button(menuDisplay, (50, 275), (300, 100), "New Game", "Left")
    ServerButton = Button(menuDisplay, (50, 425), (300, 100), "Select Server", "Left")
    SettingsButton = Button(menuDisplay, (50, 575), (300, 100), "Settings", "Left")
    ExitButton = Button(menuDisplay, (1280-50-300, 125), (300, 100), "Exit", "Right")

    while running and not breaked:
        menuDisplay.fill((0, 0, 0))
        menuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(menuDisplay, skip=True)
        
        menuDisplay.fill((0, 0, 0, 0))
        LoadButton.Update()
        NewButton.Update()
        ServerButton.Update()
        SettingsButton.Update()
        ExitButton.Update()
        
        Display_Window(menuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if LoadButton.over:
                    if GUI_Load(menuDisplay): breaked = True
                elif NewButton.over:
                    if GUI_New(menuDisplay): breaked = True
                elif ServerButton.over: GUI_Server(menuDisplay)
                elif SettingsButton.over: GUI_Options(menuDisplay)
                elif ExitButton.over: running = False

        clock.tick(FPS)

# TODO Load game menu function
def GUI_Load(menuDisplay):
    global running
    breaked = False
    LmenuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    LmenuDisplay.fill((0, 0, 0, 0))
    Save1Button = Button(LmenuDisplay, (50, 50), (300, 100), "Load Save", SCALE)
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
    NmenuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    NmenuDisplay.fill((0, 0, 0, 0))
    Save1Button = Button(NmenuDisplay, (50, 50), (300, 100), "New Save", SCALE)
    Save1Button.Update()

    SliderAnimation(display, menuDisplay, NmenuDisplay, "Left")

    while running and not breaked:
        NmenuDisplay.fill((0, 0, 0))
        NmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(NmenuDisplay, skip=True)

        NmenuDisplay.fill((0, 0, 0, 0))
        Save1Button.Update()
        Display_Window(NmenuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SliderAnimation(display, NmenuDisplay, menuDisplay, "Right")
                    breaked = True
                    break

# TODO Server select menu function
def GUI_Server(menuDisplay):
    global running
    breaked = False
    SmenuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    SmenuDisplay.fill((0, 0, 0, 0))
    Server1Button = Button(SmenuDisplay, (50, 50), (300, 100), "a server", SCALE)
    Server1Button.Update()

    SliderAnimation(display, menuDisplay, SmenuDisplay, "Right")

    while running and not breaked:
        SmenuDisplay.fill((0, 0, 0))
        SmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(SmenuDisplay, skip=True)

        SmenuDisplay.fill((0, 0, 0, 0))
        Server1Button.Update()
        Display_Window(SmenuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SliderAnimation(display, SmenuDisplay, menuDisplay, "Left")
                    breaked = True
                    break

# TODO Options menu function
def GUI_Options(menuDisplay):
    global running
    breaked = False
    OmenuDisplay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    OmenuDisplay.fill((0, 0, 0, 0))
    Options1Button = Button(OmenuDisplay, (50, 50), (300, 100), "a Option", SCALE)
    Options1Button.Update()

    SliderAnimation(display, menuDisplay, OmenuDisplay, "Down")

    while running and not breaked:
        OmenuDisplay.fill((0, 0, 0))
        OmenuDisplay.blit(Constants.BACKGROUND, (0, 0))
        Display_Window(OmenuDisplay, skip=True)

        OmenuDisplay.fill((0, 0, 0, 0))
        Options1Button.Update()
        Display_Window(OmenuDisplay, absolute=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SliderAnimation(display, OmenuDisplay, menuDisplay, "Up")
                    breaked = True
                    break

# TODO Ingame pause menu function
def IGGUI_Pause():
    pass

# TODO Main game loop
def Main():
    GUI_Main()

Main()

pygame.quit()