# Import python librarys
from typing_extensions import runtime
import pygame, pickle

# Set a few constants
FPS = 60
VEL = 5
BULLET_VEL = 40
WIDTH, HEIGT = 1280, 720

# Open settings file
with open("Settings.txt", "rb") as settingsfile:
    try: settings = pickle.load(settingsfile)
    except EOFError: settings = {
        "Resolution":(1280, 720), # Resolution in (width, heigt)
        "Fullscreen":False, # if fullscreen is enabled
        "Server":0, # index in Servers
        "Servers":[{"Name":"official", "Host":"127.0.0.1", "Port":65432}]} # list of servers

# Start pygame window
pygame.init()
running = True
window = pygame.display.set_mode(settings["Resolution"])
display = pygame.Surface((WIDTH, HEIGT))
print(display.get_rect().center)
pygame.display.set_caption("PyThing")

# import local librarys
import Constants

# Function for connecting with the server
def Connect():
    pass

# Function for disconnecting with the server
def Disconnect():
    pass

# Function to scale the display correctly
def Display_Window(display):
    window.fill((0, 0, 0))
    width, heigt = settings["Resolution"]

    # If the aspact ratio is the same as original image
    if width / WIDTH == heigt / HEIGT:
        window.blit(
            pygame.transform.scale(display,
                (width, heigt)), # Just scale the image to the new resolution
                (0, 0))

    # If the heigt is higher than normal
    elif width / WIDTH < heigt / HEIGT:
        #FPos = frame.get_rect().center
        #FPos = width / 2 - FPos[0], 0
        #window.blit(pygame.transform.scale(display, (int(WIDTH * heigt / HEIGT), heigt)), FPos)
        pass


    elif width / WIDTH > heigt / HEIGT:
        frame = pygame.transform.scale(display, (width, int(HEIGT * width / WIDTH)))
        FPos = frame.get_rect().center
        FPos = 0, heigt / 2 - FPos[1]
        window.blit(frame, FPos)
    pygame.display.update()

# Main menu function
def GUI_Main():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        window.fill((0, 0, 0))
        window.blit(Constants.BACKGROUND, (0, 0))
        pygame.display.update()

# Load game menu function
def GUI_Load():
    pass

# New game menu function
def GUI_New():
    pass

# Server select menu function
def GUI_Server():
    pass

# Options menu function
def GUI_Options():
    pass

# Pause menu function
def IGGUI_Pause():
    pass

# TODO Main game loop
def Main():
    GUI_Main()

Main()

pygame.quit()