# Universidad del Valle de Guatemala
# Sara Nohemi Zavala Gutierrez
# Graficas por computador
# 18893 - Proyecto 3


import pygame
import sys
from math import pi, cos, sin, atan2
import time

# ---------------------------------------------------------
SPRITE_BACKGROUND = (152, 0, 136, 255)
buttonsColor = (209, 101, 44)
onSelectedButton = (85, 180, 144)
onSelectedTextColor = (250, 250, 250)
textColor = (0, 0, 0)
GRASS = (89,159,13)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ---------------------------------------------------------
# images, walls and enemies
# ---------------------------------------------------------
back = pygame.image.load('./images/main.jpg')
inst = pygame.image.load('./images/inst.jpg')
wall1 = pygame.image.load('./images/wall1.png')
wall2 = pygame.image.load('./images/wall2.jpg')
wall3 = pygame.image.load('./images/wall3.jpg')
wall4 = pygame.image.load('./images/wall4.png')
wall5 = pygame.image.load('./images/wall5.png')

# Enemies
# ---------------------------------------------------------`
enemy1 = pygame.image.load('./images/sprite1.png')
enemy2 = pygame.image.load('./images/sprite2.png')
enemy3 = pygame.image.load('./images/sprite3.png')
enemy4 = pygame.image.load('./images/sprite4.png')
player_hand = pygame.image.load('./images/player.png')

textures = {
    "1": wall1,
    "2": wall2,
    "3": wall3,
    "4": wall4,
    "5": wall5,
    # "6": end
}
enemies = [
    {
        "x": 100,
        "y": 200,
        "texture": enemy1
    },
    {
        "x": 280,
        "y": 190,
        "texture": enemy2
    },
    {
        "x": 225,
        "y": 340,
        "texture": enemy3
    },
    {
        "x": 220,
        "y": 425,
        "texture": enemy4
    },
    {
        "x": 320,
        "y": 420,
        "texture": enemy1
    }
]

pygame.init()
screen = pygame.display.set_mode((1000, 500))


class Raycaster:
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.map = []
        self.zbuffer = [-float('inf') for z in range(int(self.width))]
        self.player = {
            "x": self.blocksize + 20,
            "y": self.blocksize + 20,
            "a": 0,
            "fov": pi / 3
        }

    def main_menu_sound(self):
        pygame.mixer.music.load('./music/01_Circle_of_Life.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def point(self, x, y, c=None):
        screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture, size):
        x = int(x)
        y = int(y)
        size = int(size)
        for cx in range(x, x + size):
            cx = int(cx)
            for cy in range(y, y + size):
                cy = int(cy)
                tx = int((cx - x) * 12.8)
                ty = int((cy - y) * 12.8)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    def draw_player(self, xi, yi, w=256, h=256):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 32 / w)
                ty = int((y - yi) * 32 / h)
                c = player_hand.get_at((tx, ty))
                if c != (152, 0, 136, 255):
                    self.point(x, y, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0
        cosa = cos(a)
        sina = sin(a)
        while True:
            x = int(self.player["x"] + d * cosa)
            y = int(self.player["y"] + d * sina)

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * 50
                hity = y - j * 50
                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * 2.56)
                return d, self.map[j][i], tx
            self.screen.set_at((int(x/2), int(y/2)), WHITE)
            d += 1

    def draw_stake(self, x, h, tx, texture):
        h_half = h / 2
        start = int(250 - h_half)
        end = int(250 + h_half)
        end_start_pro = 128 / (end - start)
        for y in range(start, end):
            ty = int((y - start) * end_start_pro)
            c = texture.get_at((tx, ty))
            self.point(x, y, c)

    def draw_sprite(self, sprite):
        sprite_a = atan2((sprite["y"] - self.player["y"]),
                         (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"]) ** 2 +
                    (self.player["y"] - sprite["y"]) ** 2) ** 0.5
        sprite_size_half = int(250 / sprite_d * 70)
        sprite_size = sprite_size_half * 2
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 477.46 +
                       250 - sprite_size_half)
        sprite_y = int(250 - sprite_size_half)

        sprite_size_pro = 128 / sprite_size
        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] <= sprite_d:
                    tx = int((x - sprite_x) * sprite_size_pro)
                    ty = int((y - sprite_y) * sprite_size_pro)
                    c = sprite["texture"].get_at((tx, ty))
                    if c != (152, 0, 136, 255):
                        self.point(x, y, c)
                        self.zbuffer[x - 500] = sprite_d

    def coords(self):
        font = pygame.font.SysFont("forte", 25, False)
        coords = "X: " + str(r.player["x"]) + "   Y: " + str(r.player["y"])
        coords_text = font.render(coords, 1, pygame.Color(58,166,166))
        return coords_text

    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for i in range(0, 1000):
            a = self.player["a"] - self.player["fov"] / 2 + (i * 0.00105)
            d, m, tx = self.cast_ray(a)
            x = i
            h = (500 / (d * cos(a - self.player["a"]))) * 50
            self.draw_stake(x, h, tx, textures[m])

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':

                    self.draw_rectangle(x/2, y/2, textures[self.map[j][i]], self.blocksize/2)

        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], BLACK)
            self.draw_sprite(enemy)

        self.point(int(self.player["x"] * 0.2) + 900, int(self.player["y"] * 0.2) + 400, (255,255,255))

        # self.draw_player(466, 244, player_hand)

    def drawText(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def main_menu(self):
        tittle_font = pygame.font.SysFont('gabriola', 50, True)
        textFont = pygame.font.SysFont("Cambria", 30)
        isClicked = False
        self.main_menu_sound()
        screen_img = back
        intro = True
        while intro:
            screen.blit(screen_img, [-1, 0])
            r.drawText("Lion King", tittle_font, WHITE, screen, 415, 100)
            x, y = pygame.mouse.get_pos()

            startGameBtn = pygame.Rect(410, 200, 200, 50)
            if startGameBtn.collidepoint((x, y)):
                pygame.draw.rect(screen, onSelectedButton, startGameBtn)
                r.drawText("Play", textFont, onSelectedTextColor, screen, 480, 205)
                if isClicked:
                    self.start_game()
            else:
                pygame.draw.rect(screen, buttonsColor, startGameBtn)
                r.drawText("Play", textFont, textColor, screen, 480, 205)
            # -------------------------------------------------------------------------------------------------
            instBtn = pygame.Rect(410, 300, 200, 50)
            if instBtn.collidepoint((x, y)):
                pygame.draw.rect(screen, onSelectedButton, instBtn)
                r.drawText("Instructions", textFont, onSelectedTextColor, screen, 430, 305)
                if isClicked:
                    self.instructionsPage()
            else:
                pygame.draw.rect(screen, buttonsColor, instBtn)
                r.drawText("Instructions", textFont, textColor, screen, 430, 305)
            # -------------------------------------------------------------------------------------------------
            exitBtn = pygame.Rect(410, 400, 200, 50)
            if exitBtn.collidepoint((x, y)):
                pygame.draw.rect(screen, onSelectedButton, exitBtn)
                r.drawText("Exit", textFont, onSelectedTextColor, screen, 480, 405)
                if isClicked:
                    pygame.quit()
                    sys.exit()
            else:
                pygame.draw.rect(screen, buttonsColor, exitBtn)
                r.drawText("Exit", textFont, textColor, screen, 480, 405)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        isClicked = True

            pygame.display.update()

    def instructionsPage(self):
        screen_img = inst
        screen.blit(screen_img, [-1, 0])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.K_3:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.main_menu()

            # Fonts --------------------
            instruction_tittle = pygame.font.SysFont('gabriola', 50, True)
            return_key = pygame.font.SysFont('gabriola', 25, True)
            message = pygame.font.SysFont('inkfree', 35, False, True)
            description = pygame.font.SysFont('couriernew', 20, False, False)
            option = pygame.font.SysFont('lucidasanstypewriter', 15, False, False)

            TextSurf, TextRect = self.text_objects("Instrucciones", instruction_tittle)
            TextRect.center = (int(self.width / 2), int(self.height / 4))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Bienvenido! El objetivo del juego es llegar a la roca del Rey!.",
                                                   description)
            TextRect.center = (int(self.width / 2), int(self.height / 3))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Trata de no toparte con paredes o hienas, de lo contrario",
                                                   description)
            TextRect.center = (int(self.width / 2), int(self.height / 2.5))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Simba morirá y perderá su progreso", description)
            TextRect.center = (int(self.width / 2), int(self.height / 2.10))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Controles: W A D S ", description)
            TextRect.center = (int(self.width / 2), int(self.height / 1.75))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Hakuna matata", message)
            TextRect.center = (int(self.width / 1.5), int(self.height / 1.5))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = self.text_objects("Presiona R para regresar", return_key)
            TextRect.center = (int(self.width / 4), int(self.height / 1.5))
            screen.blit(TextSurf, TextRect)

            pygame.display.update()
            clock.tick(15)

    def game_over(self):
        pass

    def game_win(self):
        pass

    def update_fps(self):
        font = pygame.font.SysFont("erasitc", 25, True)
        fps = "FPS: " + str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("black"))
        return fps_text

    def start_game(self):
        paused = False
        running = True
        while running:
            screen.fill((0, 0, 0))
            d = 10
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    exit(0)
                if e.type == pygame.KEYDOWN:
                    if not paused:
                        if e.key == pygame.K_a:
                            r.player["a"] -= 0.157
                        if e.key == pygame.K_d:
                            r.player["a"] += 0.157
                        if e.key == pygame.K_w:
                            r.player["x"] += int(d * cos(r.player["a"]))
                            r.player["y"] += int(d * sin(r.player["a"]))
                        if e.key == pygame.K_s:
                            r.player["x"] -= int(d * cos(r.player["a"]))
                            r.player["y"] -= int(d * sin(r.player["a"]))

                    if e.key == pygame.K_SPACE:
                        paused = not paused
                if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                    if not paused:
                        if e.button == 4:
                            r.player['a'] -= 0.157
                        if e.button == 5:
                            r.player['a'] += 0.157

            screen.fill(pygame.Color("LIGHTSKYBLUE"), (0, 0, int(r.width), int(r.height / 2)))
            screen.fill(GRASS, (0, int(r.height / 2), int(r.width), int(r.height / 2)))
            r.render()
            screen.blit(self.update_fps(), (10, 10))
            clock.tick(30)
            pygame.display.update()



screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./level1.txt')
pygame.display.set_caption('Zaravala')
inst = pygame.transform.scale(inst, (r.width, r.height))
back = pygame.transform.scale(back, (r.width, r.height))
clock = pygame.time.Clock()
r.main_menu()
