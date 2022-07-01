# General terms:
# OSR: Original Screen Resolution (Speaks for itself)
# SR: Screen Resolution (the resolution the game is displayed in)

import pygame, pickle, time, socket, threading

with open("Settings.txt", "rb") as settingsfile: # Open Settings file
    try: settings = pickle.load(settingsfile)
    except EOFError: settings = {
        "Resolution":(1280, 720), # Resolution in [width, height]
        "Fullscreen":False, # if fullscreen is enabled
        "Server":0, # index in Servers
        "Servers":[{"Name":"Official", "Host":"127.0.0.1", "Port":65432}]} # list of servers

FPS = 60 # Frames per second (com'on you know this)
VEL = 5 # Player velocity
BULLET_VEL = 40 # Bullet velocity
WIDTH, HEIGHT = 1280, 720 # ORS
SCALE = WIDTH / settings["Resolution"][0], HEIGHT / settings["Resolution"][1] # Scale of the SR to the OSR
INSCALE = settings["Resolution"][0] / WIDTH, settings["Resolution"][1] / HEIGHT # Scale of OSR to the SR

pygame.init()
running = True
window = pygame.display.set_mode(settings["Resolution"])
display = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.display.set_caption("PyThing")

import Constants

class Server:
    def __init__(self, name, ip, port, operation):
        self.NAME = name # Name of the server
        self.IP = ip # IP of the server
        self.PORT = port # Port of the server
        self.OPERATION = operation # The opperation this instance will do
        self.SEED = None # Ingame seed of the server
        self.ping = None # Ping of the server
        self.status = None # status of the instance
        self.run = True # if the instance is running
        x = threading.Thread(target=self.Setup)
        x.start()

    def Ping(self):
        self.status = "Pinging"
        ping = pickle.dumps(1) # Define a message
        while self.run:
            t = time.perf_counter() # Start a timer
            self.socket.send(ping) # Send message
            self.socket.recv(2048) # Wait for awnser
            t2 = time.perf_counter() # Stop time
            self.ping = int((t2-t)*1000) # Calculate the time it took
            time.sleep(.5)

    def Setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Start the socket connection
        while self.run: 
            try: self.socket.connect((self.IP, self.PORT)) # Try to connect
            except ConnectionRefusedError: time.sleep(1); self.ping = "N/A"; self.status = "Can't connect" # If refused try again
            else: # If succses proceed with operation
                self.status = "Connected"
                if self.OPERATION == "Ping": self.Ping()
        self.status = "Stopped"

class Button:
    def __init__(self, display, position, size, text, side=None, backgroundcolor=(100, 100, 100, 200), textcolor=(0, 0, 0), textsize=32):
        self.DISPLAY = display # Display to use
        self.X, self.Y = position # Position at north-west
        self.WIDTH, self.HEIGHT = size # Size in pixels
        self.TEXT = text # Text to display
        self.BACKGROUND = backgroundcolor # The color of the background
        self.TEXTCOLOR = textcolor # The color of the text
        self.TEXTSIZE = textsize # The size of the text
        self.SIDE = side # Side that the button won't expand

        # Set the correct update function for the side the button will be expanding to
        if side == "Left": self.UPDATE = self.UpdateLeft
        elif side == "Right": self.UPDATE = self.UpdateRight
        else: self.UPDATE = self.UpdateNone

        self.over = False # True if mouse is over button
        self.scale = 1 # Scale factor when mouse is over button

        self.MakeImage()

    def UpdateLeft(self):
        self.rect.width, self.rect.height = int(self.WIDTH * self.scale), int(self.HEIGHT * self.scale) # Simply Scaling the border accordingly
        self.rect.y = self.Y - (self.rect.height - self.HEIGHT) / 2 # Move the button [(ScaledHeight - OriginalHeight) / 2] pixels up accordingly
        self.DISPLAY.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.X, self.rect.y)) # Simply Scale and blit the image
        pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5) # Draw the border
        mousepos = pygame.mouse.get_pos() # Get the position of the mouse
        if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))): # Check if the mouse is over the button
            if self.scale < 1.5: self.scale += 0.1 # If the scale factor is less then max and the mouse is over the button increase
            self.over = True
        else:
            if self.scale > 1: self.scale -= 0.1 # If the mouse is not over the button reset scale factor
            self.over = False
            
    def UpdateRight(self):
        self.rect.width, self.rect.height = int(self.WIDTH * self.scale), int(self.HEIGHT * self.scale) # Simply Scaling the border accordingly
        self.rect.y = self.Y - (self.rect.height - self.HEIGHT) / 2 # Move the button [(ScaledHeight - OriginalHeight) / 2] pixels up accordingly
        self.rect.x = self.X - (self.rect.width - self.WIDTH) # Move the button [(ScaledWidth - OriginalWidth)] pixels to the right
        self.DISPLAY.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y)) # Simply Scale and blit the image
        pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5) # Draw the border
        mousepos = pygame.mouse.get_pos() # Get the position of the mouse
        if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))): # Check if the mouse is over the button
            if self.scale < 1.5: self.scale += 0.1 # If the scale factor is less then max and the mouse is over the button increase
            self.over = True
        else:
            if self.scale > 1: self.scale -= 0.1 # If the mouse is not over the button reset scale factor
            self.over = False

    def UpdateNone(self):
        self.DISPLAY.blit(self.image, (self.X, self.Y)) # Blit the background
        pygame.draw.rect(self.DISPLAY, (0, 0, 0), self.rect, 5) # Draw the border
        mousepos = pygame.mouse.get_pos() # Get the position of the mouse
        if self.rect.collidepoint((int(mousepos[0]*SCALE[0]), int(mousepos[1]*SCALE[1]))): self.over = True # Check if the mouse is over the button
        else: self.over = False

    def Update(self):
        self.UPDATE()

    def MakeImage(self):
        self.rect = pygame.Rect((self.X, self.Y), (self.WIDTH, self.HEIGHT)) # Make the rect
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA) # Make the empty image
        self.image.fill(self.BACKGROUND) # Fill the image with the background color
        self.textImage = Constants.GetFont(self.TEXTSIZE).render(self.TEXT, 0, self.TEXTCOLOR) # Render the text
        self.image.blit(self.textImage, self.textImage.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))) # Blit the text on the image

# Function to scale the display correctly
def Display_Window(display, skip=False, absolute=False):
    width, height = settings["Resolution"]

    # If the SCALE (SR to OSR) is the same
    if INSCALE[0] == INSCALE[1] or absolute:
        frame = pygame.transform.scale(display, (width, height)) # Just scale the image to the SR
        window.blit(frame, (0, 0)) # Because of the same size it can stay at the same place

    # If the SR is higher then ORS
    elif INSCALE[0] < INSCALE[1]:
        frame = pygame.transform.scale(display, (int(WIDTH * INSCALE[1]), height)) # Make the image [height / HEIGHT] times wider so the aspect ratio is conserved
        window.blit(frame, ((width - frame.get_width())/2, 0)) # Place the image [width - Newidth] pixels to the left

    # If the SR in wider then ORS
    elif INSCALE[0] > INSCALE[1]:
        frame = pygame.transform.scale(display, (width, int(HEIGHT * INSCALE[0]))) # Make the image [width / WIDTH] times higher so the aspect ratio is conserved
        window.blit(frame, (0, (height - frame.get_height())/2)) # Place the image [height - NewHeight] pixels up
    if not skip: pygame.display.update()

# Funtion to slide the screen in a direction
def SliderAnimation(display, startingDisplay, endingDisplay, direction):
    position, speed = 0, 0 # Make local variables

    while direction == "Up": # If the direction is Up use this loop
        if position <= 360: speed += 1 # If the animation is less then half done increase speed
        elif speed > 1:  speed -= 1 # If the animation is more then half done decrease speed
        if position+speed > HEIGHT: break # If the animation is done break
        else: position += speed # If the animation is not done add speed to position
        display.blit(Constants.BACKGROUND, (0, position/2)) # Blit the upper background
        display.blit(Constants.BACKGROUND, (0, position/2-HEIGHT)) # Blit the lower background
        Display_Window(display, skip=True) # Display the backgrounds
        display.fill((0, 0, 0, 0)) # Make the screen black
        display.blit(startingDisplay, (0, position)) # Blit the starting display
        display.blit(endingDisplay, (0, position-HEIGHT)) # Blit the ending display
        Display_Window(display, absolute=True) # Show everything on screen

    while direction == "Down": # If the direction is Up use this loop
        if position <= 360: speed += 1 # If the animation is less then half done increase speed
        elif speed > 1:  speed -= 1 # If the animation is more then half done decrease speed
        if position+speed > HEIGHT: break # If the animation is done break
        else: position += speed # If the animation is not done add speed to position
        display.blit(Constants.BACKGROUND, (0, 0-position/2)) # Blit the upper background
        display.blit(Constants.BACKGROUND, (0, 0-position/2+HEIGHT)) # Blit the lower background
        Display_Window(display, skip=True) # Display the backgrounds
        display.fill((0, 0, 0, 0)) # Make the screen black
        display.blit(startingDisplay, (0, 0-position)) # Blit the starting display
        display.blit(endingDisplay, (0, 0-position+HEIGHT)) # Blit the ending display
        Display_Window(display, absolute=True) # Show everything on screen

    while direction == "Left": # If the direction is Up use this loop
        if position <= 640: speed += 1 # If the animation is less then half done increase speed
        elif speed > 1:  speed -= 1 # If the animation is more then half done decrease speed
        if position+speed > WIDTH: break # If the animation is done break
        else: position += speed # If the animation is not done add speed to position
        display.blit(Constants.BACKGROUND, (position/2, 0)) # Blit the right background
        display.blit(Constants.BACKGROUND, (position/2-WIDTH, 0)) # Blit the left background
        Display_Window(display, skip=True) # Display the backgrounds
        display.fill((0, 0, 0, 0)) # Make the screen black
        display.blit(startingDisplay, (position, 0)) # Blit the starting display
        display.blit(endingDisplay, (position-WIDTH, 0)) # Blit the ending display
        Display_Window(display, absolute=True) # Show everything on screen
        
    while direction == "Right": # If the direction is Up use this loop
        if position <= 640: speed += 1 # If the animation is less then half done increase speed
        elif speed > 1:  speed -= 1 # If the animation is more then half done decrease speed
        if position+speed > WIDTH: break # If the animation is done break
        else: position += speed # If the animation is not done add speed to position
        display.blit(Constants.BACKGROUND, (0-position/2, 0)) # Blit the left background
        display.blit(Constants.BACKGROUND, (0-position/2+WIDTH, 0)) # Blit the right background
        Display_Window(display, skip=True) # Display the backgrounds
        display.fill((0, 0, 0, 0)) # Make the screen black
        display.blit(startingDisplay, (0-position, 0)) # Blit the starting display
        display.blit(endingDisplay, (0-position+WIDTH, 0)) # Blit the ending display
        Display_Window(display, absolute=True) # Show everything on screen

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
    ExitButton = Button(menuDisplay, (930, 125), (300, 100), "Exit", "Right")
    Text = Button(menuDisplay, (440, 5), (400, 75), "PyThing", textsize=60, backgroundcolor=(100, 100, 100, 200))

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
        Text.Update()
        
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
    server = Server('Official', '127.0.0.1', 65432, "Ping")
    GUI_Main()
    server.run = False

Main()

pygame.quit()