from tkinter.constants import LEFT, RIGHT
import pygame, os, Modules, socket, pickle, math, tkinter, random

from pygame.constants import FULLSCREEN
from tkinter import Variable, ttk

pygame.display.init()
ChestOpen = 0
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
FPS = 60
VEL = 5
BULLET_VEL = 40
WIDTH, HEIGT = 1280, 720 
rel_x, rel_y = 0, 0
Mplayer = None
s = None
with open("Saves.txt", "rb") as savesfile:
    try:
        saves = pickle.load(savesfile)
    except EOFError:
        saves = []

with open("Settings.txt", "rb") as settingsfile:
    try:
        settings = pickle.load(settingsfile)
    except EOFError:
        settings = []

class StartupWindow():
    global Mplayer
    def __init__(self, master):
        self.Saves = []
        for i in saves:
            self.Saves.append(i.Name)
        while len(self.Saves) < 5:
            self.Saves.append("Empty save")
        if len(settings) == 0:
            self.SWIDTH, self.SHEIGT = 1280, 720
            self.Fullscreen = False
        else:
            self.Fullscreen = settings[0]
            self.SWIDTH, self.SHEIGT = settings[1], settings[2]
        self.master = master
        master.title("Startup")

        self.WelcomeLabel = tkinter.Label(master, text="Welcome to PyThing!")
        self.WelcomeLabel.pack()

        self.ConfirmButton = tkinter.Button(master, text="Start new game", command=self.NewGame)
        self.ConfirmButton.pack()

        self.ContinueButton = tkinter.Button(master, text="Load save", command=self.LoadSave)
        self.ContinueButton.pack()
        
        self.SettingsButton = tkinter.Button(master, text="Settings", command=self.Settings)
        self.SettingsButton.pack()
        
    def LoadSave(self):
        self.Lroot = tkinter.Tk()
        self.LWindow = SaveWindow(self.Lroot)
        root.mainloop()

    def NewGame(self):
        self.Nroot = tkinter.Tk()
        self.NWindow = NewGameWindow(self.Nroot)
        root.mainloop()

    def Settings(self):
        self.Sroot = tkinter.Tk()
        self.SWindow = SettingsWindow(self.Sroot)
        root.mainloop()

    def OnClose():
        if s != None:
            s.send(pickle.dumps("Stop"))
        exit()

class SettingsWindow():
    def __init__(self, master):
        self.master = master
        master.title("Settings")

        self.ResolutionLabel = tkinter.Label(master, text="Resolution")
        self.ResolutionLabel.pack()

        self.FullscreenCheckbox = tkinter.Checkbutton(master, text="Fullscreen", command=self.FullscreenF)
        self.FullscreenCheckbox.pack()

        self.ResolutionBox = ttk.Combobox(master, values=["1280x720", "1440x900", "1680x1050", "1920x1080"], state="enabled")
        self.ResolutionBox.set(str(Window.SWIDTH) + "x" + str(Window.SHEIGT))
        if Window.Fullscreen:
            self.FullscreenCheckbox.select()
            self.ResolutionBox.configure(state="disabled")
        self.ResolutionBox.pack()


        self.OKButton = tkinter.Button(master, text="Ok", command=self.OK)
        self.OKButton.pack()
    def FullscreenF(self):
        Window.Fullscreen = not Window.Fullscreen
        if Window.Fullscreen == 1:
            self.ResolutionBox.configure(state="disabled")
        else:
            self.ResolutionBox.configure(state="enabled")
    def OK(self):
        if Window.Fullscreen:
            Res = pygame.display.Info()
            Window.SWIDTH, Window.SHEIGT = Res.current_w, Res.current_h
        else:
            Res = self.ResolutionBox.get().split("x")
            Window.SWIDTH, Window.SHEIGT = int(Res[0]), int(Res[1])
        with open("Settings.txt", "wb") as settingsfile:
            pickle.dump([Window.Fullscreen, Window.SWIDTH, Window.SHEIGT], settingsfile)
        Window.Sroot.destroy()

class SaveWindow():
    def __init__(self, master):
        self.master = master
        master.title("Load save")

        self.SavesLabel = tkinter.Label(master, text="Load save")
        self.SavesLabel.pack()

        a = 0

        self.Listbox = tkinter.Listbox(master, height=5)
        for i in Window.Saves:
            a += 1
            self.Listbox.insert(a, i)
        self.Listbox.pack()

        self.ContinueButton = tkinter.Button(master, text="Continue!", command=self.LoadSave)
        self.ContinueButton.pack()
    def LoadSave(self):
        global Mplayer, s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            server = pickle.loads(s.recv(2048))
            name = self.Listbox.get(tkinter.ACTIVE)
            if name != "":
                if name != "Empty save":
                    if name not in server.PlayerNames:
                        for i in saves:
                            if i.Name == name:
                                Mplayer = i
                        root.destroy()
                        Window.Lroot.destroy()
                        try:
                            Window.Sroot.destroy()
                        except:
                            pass
                        try:
                            Window.Nroot.destroy()
                        except:
                            pass
                    else:
                        self.SavesLabel.config(text="That name is in use.")
                else:
                    self.SavesLabel.config(text="Not a active save.")
            else:
                self.SavesLabel.config(text="Please select a save.")
        except ConnectionRefusedError:
            self.SavesLabel.config(text="Could not connect to server.")

class NewGameWindow():
    def __init__(self, master):
        self.master = master
        master.title("New Game")

        self.NewGameLabel = tkinter.Label(master, text="Start a new game")
        self.NewGameLabel.pack()

        self.NameLabel = tkinter.Label(master, text="Enter your name:")
        self.NameLabel.pack()

        self.NameEntry = tkinter.Entry(master)
        self.NameEntry.pack()

        self.SaveLabel = tkinter.Label(master, text="Select save:")
        self.SaveLabel.pack()

        self.Listbox = tkinter.Listbox(master, height=5)
        a = 0
        for i in Window.Saves:
            a += 1
            self.Listbox.insert(a, i)
        self.Listbox.pack()

        self.ConfirmButton = tkinter.Button(master, text="Confirm!", command=self.NewGame)
        self.ConfirmButton.pack()
    def NewGame(self):
        global Mplayer, s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            server = pickle.loads(s.recv(2048))
            name = self.NameEntry.get()
            save = self.Listbox.get(tkinter.ACTIVE)
            if name != "" and name != "Empty save":
                if name not in Window.Saves:
                    if name not in server.PlayerNames:
                        if save in Window.Saves and save != "Empty save":
                            Window.Saves[Window.Saves.index(save)] = name
                        Mplayer = Modules.Player(name)
                        root.destroy()
                        Window.Nroot.destroy()
                        try:
                            Window.Lroot.destroy()
                        except:
                            pass
                        try:
                            Window.Sroot.destroy()
                        except:
                            pass
                    else:
                        self.NameLabel.config(text="That name is in use.")
                else:
                    self.NameLabel.config(text="Name already in saves")
            else:
                self.NameLabel.config(text="Please enter a name.")
        except ConnectionRefusedError:
            self.NameLabel.config(text="Could not connect to server.")

root = tkinter.Tk()
Window = StartupWindow(root)
root.protocol("WM_DELETE_WINDOW", StartupWindow.OnClose)
root.mainloop()

Guns = [{"Name":"MPX", "Cal":"9x19", "Damage":30, "Sound":None, "RPM":850, "Mag":30},
{"Name":"P90", "Cal":"5.7x28", "Damage":26, "Sound":None, "RPM":900, "Mag":50},
{"Name":"MP7", "Cal":"4.6x30", "Damage":31, "Sound":None, "RPM":950, "Mag":30},
{"Name":"AK47", "Cal":"7.62x39", "Damage":42, "Sound":None, "RPM":600, "Mag":30},
{"Name":"AK74", "Cal":"5.45x39", "Damage":34, "Sound":None, "RPM":650, "Mag":30}]

SCALEX, SCALEY = Window.SWIDTH / WIDTH, Window.SHEIGT / HEIGT
pygame.font.init()
pygame.mixer.init()
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'Icon.png')))
WIN = pygame.display.set_mode((Window.SWIDTH, Window.SHEIGT))
WINI = pygame.Surface((WIDTH, HEIGT))
if Window.Fullscreen:
    pygame.display.toggle_fullscreen()
Maps = [[0, 0],[1, 0],[1, 1],[0, 1],[-1, 1],[-1, 0],[-1, -1],[0, -1],[1, -1]]
Icon = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'PlayerIcon.png')).convert_alpha(), 0)
Background = pygame.image.load(os.path.join('Assets', 'Background.png')).convert()
Pmask = pygame.mask.from_surface(Icon)
Chest = [pygame.image.load(os.path.join('Assets', 'ChestClosed.png')).convert_alpha(),
pygame.image.load(os.path.join('Assets', 'ChestOpen.png')).convert_alpha()]
FONT = pygame.font.Font(os.path.join('Assets', 'Font.ttf'), 25)
C9x19 = pygame.image.load(os.path.join('Assets', '9x19.png')).convert_alpha()

Rooms = [
pygame.image.load(os.path.join('Assets', 'Room4_90.png')).convert_alpha(),
pygame.image.load(os.path.join('Assets', 'Room3_90.png')).convert_alpha(),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room3_90.png')).convert_alpha(), 90),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room3_90.png')).convert_alpha(), 180),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room3_90.png')).convert_alpha(), 270),
pygame.image.load(os.path.join('Assets', 'Room2_180.png')).convert_alpha(), 
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room2_180.png')).convert_alpha(), 90),
pygame.image.load(os.path.join('Assets', 'Room2_90.png')).convert_alpha(),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room2_90.png')).convert_alpha(), 90),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room2_90.png')).convert_alpha(), 180),
pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Room2_90.png')).convert_alpha(), 270),
pygame.image.load(os.path.join('Assets', 'Stairs.png')).convert_alpha()]

Rooms3 = [5, 1, 7, 3]
Rooms4 = [1, 5, 3, 7]

pygame.display.set_caption("Blyad")

def Can_Move(overlap, MapX, MapY, Pos):
    RelPX, RelPY = Mplayer.X - MapX * 1000, Mplayer.Y - MapY * 1000
    if overlap == None:
        if Pos[0] and RelPX <= -430: Left = False
        else: Left = True
        if Pos[1] and RelPX >=  430: Right = False
        else: Right = True
        if Pos[2] and RelPY <= -430: Up = False
        else: Up = True
        if Pos[3] and RelPY >=  430: Down = False
        else: Down = True
    else:
        if RelPX <= -430 and (RelPY < -195 or RelPY > 195) or RelPX < 0 and (RelPY < -430 or RelPY > 430): Left = False
        else: Left = True
        if RelPX >= 430  and (RelPY < -195 or RelPY > 195) or RelPX > 0 and (RelPY < -430 or RelPY > 430): Right = False
        else: Right = True
        if RelPY <= -430 and (RelPX < -195 or RelPX > 195) or RelPY < 0 and (RelPX < -430 or RelPX > 430): Up = False
        else: Up = True
        if RelPY >= 430  and (RelPX < -195 or RelPX > 195) or RelPY > 0 and (RelPX < -430 or RelPX > 430): Down = False
        else: Down = True
    return Left, Right, Up, Down

def MakeMap(server):
    IsChest = False
    Pos = [False, False, False, False]
    CMapX, CMapY = None, None
    Rooms2 = [[False, False, False, False],[False, False, True, False],[True, False, False, False],
    [False, False, False, True],[False, True, False, False],[False, False, True, True],[True, True, False, False],
    [False, True, True, False],[True, False, True, False],[True, False, False, True],[False, True, False, True]]
    for i in range(0, 9):
        if Mplayer.X > 0: MapX = int((Mplayer.X + 500) / 1000)
        else: MapX = int((Mplayer.X - 500) / 1000)
        if Mplayer.Y > 0: MapY = int((Mplayer.Y + 500) / 1000)
        else: MapY = int((Mplayer.Y - 500) / 1000)
        MapX += Maps[i][0]
        MapY += Maps[i][1]
        if (MapX/10).is_integer() and (MapY/10).is_integer() and i == 0:
            Room = 11
            mask = pygame.mask.from_surface(Rooms[0])
            Pos = Rooms2[0]
            IsChest = True
            CMapX, CMapY = MapX, MapY
        elif (MapX/10).is_integer() and (MapY/10).is_integer():
            Room = 11
            IsChest = True
            CMapX, CMapY = MapX, MapY
        elif i == 0:
            random.seed(MapX * 10 + MapY + server.Seed)
            Room = random.randint(0, 10)
            mask = pygame.mask.from_surface(Rooms[0])
            Pos = Rooms2[Room]
        elif i in Rooms3:
            random.seed(MapX * 10 + MapY + server.Seed)
            Room = random.randint(0, 10)
            if Rooms2[Room][Rooms4.index(i)]: Pos[Rooms3.index(i)] = True
        else:
            random.seed(MapX * 10 + MapY + server.Seed)
            Room = random.randint(0, 10)
        WINI.blit(Rooms[Room], (MapX * 1000 + 115 - Mplayer.X, MapY * 1000 - 165 - Mplayer.Y))

    return mask, MapX - 1, MapY + 1, Pos, IsChest, CMapX, CMapY

def Shutdown():
    s.send(pickle.dumps("Stop"))
    with open("Saves.txt", "wb") as savesfile:
        if Mplayer.Name in Window.Saves:
            saves[Window.Saves.index(Mplayer.Name)] = Mplayer
        else:
            saves.append(Mplayer)
        pickle.dump(saves, savesfile)

def Multiplayer(player):
    s.send(pickle.dumps(player))
    return pickle.loads(s.recv(2048))

def Move(keys_pressed, overlap, MapX, MapY, Pos):
    x, y = pygame.mouse.get_pos()
    x = x - Window.SWIDTH / 2
    y = y - Window.SHEIGT / 2
    try:
        if x == 0 and y > 0:
            Mplayer.Rotation = 180
        elif y == 0 and x < 0:
            Mplayer.Rotation = 270
        elif y == 0 and x > 0:
            Mplayer.Rotation = 90
        else:
            Mplayer.Rotation = int(math.degrees(math.atan((y / x))))
        if x-WIDTH/2 == 0:
            Mplayer.Rotation = 180
        elif x > 0 and y < 0:
            Mplayer.Rotation += 90
        elif x > 0 and y > 0:
            Mplayer.Rotation += 90
        elif x < 0 and y > 0:
            Mplayer.Rotation += 270
        elif x < 0 and y < 0:
            Mplayer.Rotation += 270
    except:
        Mplayer.Rotation = 0
    Left, Right, Up, Down = Can_Move(overlap, MapX, MapY, Pos)
    if keys_pressed[pygame.K_a] and Left:
        Mplayer.X -= VEL
    if keys_pressed[pygame.K_d] and Right:
        Mplayer.X += VEL
    if keys_pressed[pygame.K_w] and Up:
        Mplayer.Y -= VEL
    if keys_pressed[pygame.K_s] and Down:
        Mplayer.Y += VEL

def draw_window(server, GUI, GUITYPE):
    global rel_x, rel_y

    WINI.fill((0, 0, 0))
    if Mplayer.X <= rel_x-200 or Mplayer.X >= rel_x+200:
        rel_x = Mplayer.X
    if Mplayer.Y <= rel_y-200 or Mplayer.Y >= rel_y+200:
        rel_y = Mplayer.Y
    WINI.blit(Background, (-Mplayer.X-200 + rel_x, -Mplayer.Y-200 + rel_y))

    mask, MapX, MapY, Pos, IsChest, CMapX, CMapY = MakeMap(server)
    overlap = mask.overlap(Pmask, ((Mplayer.X - MapX * 1000 + 475), (Mplayer.Y - MapY * 1000 + 475)))

    if IsChest: WINI.blit(Chest[ChestOpen], (CMapX * 1000 + 900 - Mplayer.X, CMapY * 1000 - 180 + Chest[ChestOpen].get_height() - Mplayer.Y))
    if IsChest and Chest[ChestOpen].get_rect(topleft = (CMapX * 1000 + 900 - Mplayer.X, CMapY * 1000 - 180 + Chest[ChestOpen].get_height() - Mplayer.Y)).collidepoint(pygame.mouse.get_pos()):
        text = FONT.render("Press left mouse button to open chest!", False, (255, 255, 255))
        WINI.blit(text, (WIDTH/2-text.get_width()/2, HEIGT/2 + 100))
        CanChest = True
    else:
        CanChest = False

    for i in server.Players:
        if i.Name != Mplayer.Name:
            icon = pygame.transform.rotate(Icon, i.Rotation - i.Rotation *2)
            icon2 = icon.get_rect(center = Icon.get_rect(center = (i.X - Mplayer.X + WIDTH/2, i.Y - Mplayer.Y + HEIGT/2)).center)
            WINI.blit(icon, icon2)

    icon = pygame.transform.rotate(Icon, Mplayer.Rotation - Mplayer.Rotation *2)
    icon2 = icon.get_rect(center = Icon.get_rect(center = (WIDTH/2, HEIGT/2)).center)
    WINI.blit(icon, icon2)

    if GUI:
        pass

    WIN.fill((0, 0, 0))
    if Window.SWIDTH / WIDTH == Window.SHEIGT / HEIGT:
        Frame = pygame.transform.scale(WINI, (Window.SWIDTH, Window.SHEIGT))
        WIN.blit(Frame, Frame.get_rect())
    elif Window.SWIDTH / WIDTH < Window.SHEIGT / HEIGT:
        Frame = pygame.transform.scale(WINI, (int(WIDTH * Window.SHEIGT / HEIGT), Window.SHEIGT))
        FPos = Frame.get_rect().center
        FPos = Window.SWIDTH / 2 - FPos[0], 0
        WIN.blit(Frame, FPos)
    elif Window.SWIDTH / WIDTH > Window.SHEIGT / HEIGT:
        Frame = pygame.transform.scale(WINI, (Window.SWIDTH, int(HEIGT * Window.SWIDTH / WIDTH)))
        FPos = Frame.get_rect().center
        FPos = 0, Window.SHEIGT / 2 - FPos[1]
        WIN.blit(Frame, FPos)
    pygame.display.update()
    return overlap, MapX, MapY, Pos, CanChest

def main():
    clock = pygame.time.Clock()
    run = True
    GUI = False
    GUITYPE = None
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and a[4]:
                GUI = True
                GUITYPE = "Chest"
                
        a = draw_window(Multiplayer(Mplayer), GUI, GUITYPE)
        if not GUI:
            Move(pygame.key.get_pressed(), a[0], a[1], a[2], a[3])
    Shutdown()
    pygame.quit()

if __name__ == "__main__":
    main()