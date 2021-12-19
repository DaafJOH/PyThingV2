from pygame import image, font, transform, mask
import os

GUNS = [{"Name":"MPX", "Cal":"9x19", "Damage":30, "Sound":None, "RPM":850, "Mag":30},
{"Name":"P90", "Cal":"5.7x28", "Damage":26, "Sound":None, "RPM":900, "Mag":50},
{"Name":"MP7", "Cal":"4.6x30", "Damage":31, "Sound":None, "RPM":950, "Mag":30},
{"Name":"AK47", "Cal":"7.62x39", "Damage":42, "Sound":None, "RPM":600, "Mag":30},
{"Name":"AK74", "Cal":"5.45x39", "Damage":34, "Sound":None, "RPM":650, "Mag":30}]

CASINGS = {"PistolCasing":image.load(os.path.join('Assets/Casings', 'PistolCasing.png')).convert_alpha()
}

ROOMS = [
image.load(os.path.join('Assets/Rooms', 'Room4_90.png')).convert_alpha(),
image.load(os.path.join('Assets/Rooms', 'Room3_90.png')).convert_alpha(),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room3_90.png')).convert_alpha(), 90),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room3_90.png')).convert_alpha(), 180),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room3_90.png')).convert_alpha(), 270),
image.load(os.path.join('Assets/Rooms', 'Room2_180.png')).convert_alpha(), 
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room2_180.png')).convert_alpha(), 90),
image.load(os.path.join('Assets/Rooms', 'Room2_90.png')).convert_alpha(),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room2_90.png')).convert_alpha(), 90),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room2_90.png')).convert_alpha(), 180),
transform.rotate(image.load(os.path.join('Assets/Rooms', 'Room2_90.png')).convert_alpha(), 270),
image.load(os.path.join('Assets/Rooms', 'Stairs.png')).convert_alpha()]

CHEST = [image.load(os.path.join('Assets', 'ChestClosed.png')).convert_alpha(),
image.load(os.path.join('Assets', 'ChestOpen.png')).convert_alpha()]

ICON = transform.rotate(image.load(os.path.join('Assets', 'PlayerIcon.png')).convert_alpha(), 0)
BACKGROUND = image.load(os.path.join('Assets', 'Background.png')).convert()
PMASK = mask.from_surface(ICON)

FONT = font.Font(os.path.join('Assets', 'Font.ttf'), 32)

MAPS = [[0, 0],[1, 0],[1, 1],[0, 1],[-1, 1],[-1, 0],[-1, -1],[0, -1],[1, -1]]
ROOMS3 = [5, 1, 7, 3]
ROOMS4 = [1, 5, 3, 7]
