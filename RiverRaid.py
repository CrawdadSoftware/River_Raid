"""
Made by:

   _____                       _           _    _____        __ _
  / ____|                     | |         | |  / ____|      / _| |
 | |     _ __ __ ___      ____| | __ _  __| | | (___   ___ | |_| |___      ____ _ _ __ ___
 | |    | '__/ _` \ \ /\ / / _` |/ _` |/ _` |  \___ \ / _ \|  _| __\ \ /\ / / _` | '__/ _ \
 | |____| | | (_| |\ V  V / (_| | (_| | (_| |  ____) | (_) | | | |_ \ V  V / (_| | | |  __/
  \_____|_|  \__,_| \_/\_/ \__,_|\__,_|\__,_| |_____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|


"""

import obj
import shot
import place
import cores
import ilhas
import ponte
import pygame
import random
from pygame.locals import *

# Zmienne globalne
vel_y = 2
speed = 0
vidas = 1
n_eny = 5
gazlev = 0
pontos = 0
helice = 0
delay_y = 3
eny_box = 96
mover = False
sair = False
game = False
intro = False
gaz_level = 166
hitplane = False
screen_height = 480
s_gaz_alert = "gaz_full"
width, height = 800, 600

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((width, height))
        self.voo0 = pygame.mixer.Sound("sons/voo0.wav")
        self.voo1 = pygame.mixer.Sound("sons/voo1.wav")
        self.voo2 = pygame.mixer.Sound("sons/voo2.wav")
        self.gaz1 = pygame.mixer.Sound("sons/gaz1.wav")
        self.gaz0 = pygame.mixer.Sound("sons/gaz0.wav")
        self.s_tiro = pygame.mixer.Sound("sons/tiro.wav")
        self.gaz_end = pygame.mixer.Sound("sons/gaz_end.wav")
        self.s_explode = pygame.mixer.Sound("sons/explode.wav")
        self.gaz_alert = pygame.mixer.Sound("sons/gaz_alert.wav")
        self.gaz_explode = pygame.mixer.Sound("sons/gaz_explode.wav")

        self.cor = cores.cor
        self.tiro = shot.Shot(self.win, 1, 0, 1)
        self.base = place.Place(self.win, width, 8, -100)
        self.plane = obj.Obj(self.win, 370, 420, 49, 42, 0, 0, 0)
        self.casa = [obj.Obj(self.win, -100, 0, 85, 56, 14, 0, 0) for _ in range(3)]
        self.ilha = [ilhas.Ilhas(self.win, width, 1, 0) for _ in range(3)]
        self.terra = [place.Place(self.win, width, 3, - i * 336 - 100) for i in range(3)]
        self.pontes = [ponte.Ponte(self.win, i * 485, -screen_height, 316, 77, 0, 0, 0) for i in range(3)]
        self.enemy = [obj.Obj(self.win, 0, 0, 0, 0, 0, 0, 0) for _ in range(n_eny)]

        self.data_casa = [[80, False] for _ in range(3)]
        self.data_enemy = [[100, i * eny_box - screen_height, 42, 30, 6, 1, 0] for i in range(n_eny)]
        self.data_ilha = [3, 3, 3]
        self.data_terra = [3, 3, 3]

        self.terra_intro = place.Place(self.win, width, 0, 0)
        self.pontes[2].ty = 1
        self.pontes[2].x = 312
        self.pontes[2].out = 1
        self.pontes[2].h = 68
        self.pontes[2].w = 175

    def main_menu(self):
        global sair
        menu = True

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sair = True
                    menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sair = True
                        menu = False

            self.win.fill((0, 0, 0))

            # Przycisk "Rozpocznij grę"
            pygame.draw.rect(self.win, (0, 255, 0), (width // 2 - 100, height // 2 - 60, 200, 50))
            font = pygame.font.SysFont(None, 35)
            text = font.render("Rozpocznij grę", True, (0, 0, 0))
            self.win.blit(text, (width // 2 - 80, height // 2 - 50))

            # Przycisk "Zakończ grę"
            pygame.draw.rect(self.win, (0, 255, 0), (width // 2 - 100, height // 2 + 10, 200, 50))
            text = font.render("Zakończ grę", True, (0, 0, 0))
            self.win.blit(text, (width // 2 - 70, height // 2 + 20))

            pygame.display.update()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if width // 2 - 100 < mouse[0] < width // 2 + 100:
                if height // 2 - 60 < mouse[1] < height // 2 - 10:
                    if click[0] == 1:
                        menu = False
                        self.restart()
                        self.game_loop()
                if height // 2 + 10 < mouse[1] < height // 2 + 60:
                    if click[0] == 1:
                        sair = True
                        menu = False

    def restart(self):
        global s_gaz_alert, pontos, vidas, mover, hitplane, data_ilha, data_enemy, data_terra, gaz_level, data_casa

        vidas = 3
        pontos = 0
        self.base.y = -100
        mover = False
        gaz_level = 166
        self.plane.out = False
        hitplane = False
        self.pontes[2].out = True
        s_gaz_alert = "gaz_full"

        # Zatrzymanie dźwięków
        self.voo0.stop()
        self.voo1.stop()
        self.voo2.stop()
        self.gaz_alert.stop()

        for i in range(3):
            self.terra[i].forma = 3
            self.data_terra[i] = 3
            self.terra[i].y = -i * 336 - 100
            self.casa[i].x = 80
            self.data_casa[i] = [80, False]
            self.ilha[i].y = -1600
            self.data_ilha[i] = 13

        self.data_casa[1][1] = True
        self.terra_intro.y = 100

        for i in range(n_eny):
            self.data_enemy[i] = [100, i * eny_box - screen_height, 42, 30, 6, 1, 0]
        self.data_enemy[4] = [350, -96, 81, 24, 8, 0]
        self.data_enemy[3] = [450, -192, 42, 30, 6, 0]
        self.data_enemy[1] = [500, -384, 37, 72, 11, 0]

    def game_loop(self):
        global sair, game, intro, vidas
        sair = False
        game = True
        intro = False

        while not sair:
            self.paint()
            sair = self.opned()
            if vidas < 0:
                self.main_menu()

    def opned(self):
        global game, intro, vidas, gaz_level

        if self.base.y < 238 and not game:
            intro = True
            self.base.y += 1
            for i in range(n_eny):
                self.enemy[i].y += 1
                if i < 3:
                    self.casa[i].y += 1
                    self.ilha[i].y += 1
                    self.terra[i].y += 1

        if self.base.y == -100 and self.plane.out:
            self.ler_pos()

        if self.base.y < 238 and game and intro:
            self.base.y += 1
            for i in range(n_eny):
                if self.enemy[i].y > self.base.y + 4:
                    self.enemy[i].out = True
                self.enemy[i].y += 1
                if i < 3:
                    self.casa[i].y += 1
                    self.ilha[i].y += 1
                    self.terra[i].y += 1

        if self.plane.out and not self.plane.t_expl and game and vidas > 0 and not intro:
            intro = True
            self.pontes[2].out = True
            gaz_level = 166
            self.plane.x = 370
            self.plane.ty = 0
            self.base.y = -100
            vidas -= 1
        if self.base.y == 238 and game and intro:
            self.plane.out = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
                return True
            if (e.type == KEYDOWN) and e.key == K_F2:
                self.restart()
                game = True
            if (e.type == KEYDOWN) and e.key == K_RETURN:
                game = True
                intro = False
                self.voo1.play(-1)
            if self.base.y == 238 and game and intro and (e.type == KEYDOWN):
                intro = False
                self.voo1.play(-1)

        return False

    def colidir(self, a, b):
        return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h

    def hitcortest(self, obj, cor):
        cor = hex(cor)
        cor = cor.lstrip('0x')
        cor = tuple(int(cor[i:i + int(6 / 3)], 16) for i in range(0, 6, int(6 / 3)))

        if obj.x >= 0 and obj.x + obj.w <= width and obj.y >= 0 and obj.y + obj.h <= height:
            for i in range(int(obj.w)):
                for j in range(int(obj.h)):
                    if (not i and (not j or j == int(obj.h) - 1)) or not j and i == int(obj.w) - 1:
                        if self.win.get_at((int(obj.x + i), int(obj.y + j))) == cor:
                            return True
        return False

    def salvar_pos(self):
        for i in range(n_eny):
            self.data_enemy[i][0] = self.enemy[i].x
            self.data_enemy[i][1] = self.enemy[i].y
            self.data_enemy[i][2] = self.enemy[i].w
            self.data_enemy[i][3] = self.enemy[i].h
            self.data_enemy[i][4] = self.enemy[i].ty
            self.data_enemy[i][5] = self.enemy[i].out
            if i < 3:
                self.data_terra[i] = self.terra[i].forma
                self.data_ilha[i] = self.ilha[i].forma
                self.data_casa[i][0] = self.casa[i].x
                self.data_casa[i][1] = self.casa[i].y

    def ler_pos(self):
        global game, data_ilha, data_terra, data_enemy, data_casa
        if vidas < 0:
            game = False

        for i in range(n_eny):
            self.enemy[i].x = self.data_enemy[i][0]
            self.enemy[i].y = self.data_enemy[i][1]
            self.enemy[i].w = self.data_enemy[i][2]
            self.enemy[i].h = self.data_enemy[i][3]
            self.enemy[i].ty = self.data_enemy[i][4]
            self.enemy[i].out = self.data_enemy[i][5]

        for i in range(3):
            self.casa[i].x = self.data_casa[i][0]
            self.casa[i].out = self.data_casa[i][1]
            self.terra[i].forma = self.data_terra[i]
            self.ilha[i].forma = self.data_ilha[i]
            self.casa[i].x = 80
            self.casa[i].y = -i * 350

        self.terra[0].y = 100
        self.terra_intro.y = 100

    def hittest(self):
        global hitplane, gaz_level, mover, pontos, s_gaz_alert
        t_expl = 40
        print(f"Test kolizji - Pozycja samolotu: ({self.plane.x}, {self.plane.y}), Kolizja samolotu: {hitplane}, Poziom paliwa: {gaz_level}")

        if self.hitcortest(self.tiro, self.cor[2]):
            self.tiro.y = -self.tiro.h

        if(self.hitcortest(self.plane, self.cor[2]) or hitplane or not gaz_level) and not self.plane.out:
            self.voo0.stop()
            self.voo1.stop()
            self.voo2.stop()
            mover = False
            hitplane = False
            self.plane.out = True
            self.gaz_alert.stop()
            self.plane.t_expl = 80
            s_gaz_alert = "gaz_full"
            if gaz_level:
                self.s_explode.play()
            else:
                self.gaz_explode.play()

        enehit = 0
        for i in range(n_eny):
            if self.enemy[i].ty == 5 or self.enemy[i].ty == 6 or self.enemy[i].ty == 8 or self.enemy[i].ty == 9:
                self.enemy[i].dir = -1
            else:
                self.enemy[i].dir = 1

            hit = self.enemy[i].w
            self.enemy[i].w = hit/2
            if self.hitcortest(self.enemy[i], self.cor[2]):
                if self.enemy[i].ty == 5 or self.enemy[i].ty == 6:
                    self.enemy[i].ty = 4
                    self.enemy[i].x += 2
                if self.enemy[i].ty == 8:
                    self.enemy[i].x += 2
                    self.enemy[i].ty = 7

            self.enemy[i].x += hit/2
            if self.hitcortest(self.enemy[i], self.cor[2]):
                if self.enemy[i].ty == 4 or self.enemy[i].ty == 3:
                    self.enemy[i].x -= 2
                    self.enemy[i].ty = 6
                if self.enemy[i].ty == 7:
                    self.enemy[i].x -= 2
                    self.enemy[i].ty = 8
            self.enemy[i].x -= hit/2
            self.enemy[i].w = hit

            if self.colidir(self.tiro, self.enemy[i]) and not self.enemy[i].out and self.tiro.y >= 0:
                self.enemy[i].t_expl = t_expl
                self.enemy[i].out = True
                enehit = self.enemy[i].ty
                self.s_tiro.stop()
                self.s_explode.play()
                self.tiro.y = -self.tiro.h

            if self.colidir(self.plane, self.enemy[i]) and self.enemy[i].ty < 11 and not self.enemy[i].out:
                self.enemy[i].t_expl = t_expl
                self.enemy[i].out = True
                enehit = self.enemy[i].ty
                self.s_tiro.stop()
                hitplane = True

            if self.colidir(self.plane, self.enemy[i]) and self.enemy[i].ty == 11 and not self.enemy[i].out and not self.plane.out:
                if gaz_level < 165:
                    self.gaz0.play()
                    gaz_level += 0.3
                else:
                    self.gaz1.play()

            if (self.colidir(self.plane, self.pontes[0]) or self.colidir(self.plane, self.pontes[1])) and not self.plane.out:
                hitplane = True

            if self.colidir(self.plane, self.pontes[2]) and not self.pontes[2].out:
                self.salvar_pos()
                hitplane = True
                pontos += 250
                self.pontes[2].out = True
                self.pontes[2].t_expl = t_expl

            if self.colidir(self.pontes[2], self.tiro) and not self.pontes[2].out and self.tiro.y >= 0:
                self.salvar_pos()
                self.pontes[2].t_expl = t_expl
                self.pontes[2].out = True
                pontos += 250
                self.s_tiro.stop()
                self.s_explode.play()
                self.tiro.y = -100

            if 2 < enehit < 7:
                pontos += 80
            elif 6 < enehit < 9:
                pontos += 40
            elif 8 < enehit < 11:
                pontos += 120
            elif enehit == 11:
                pontos += 30

    def inimigos(self):
        global helice, gaz_level, gazlev, s_gaz_alert

        helice = not helice
        self.hittest()
        for i in range(n_eny):
            # animacja helisy helikopterów
            if helice and self.enemy[i].ty == 3 or self.enemy[i].ty == 5:
                self.enemy[i].ty += 1
            elif self.enemy[i].ty == 4 or self.enemy[i].ty == 6:
                self.enemy[i].ty -= 1

            if game and not intro:
                # ruch wrogów w pionie
                self.enemy[i].y += mover * vel_y

                # ruch wrogów: statków i helikopterów
                if 2 < self.enemy[i].ty < 9 and self.enemy[i].y > 200 and not self.enemy[i].out:
                    self.enemy[i].x += self.enemy[i].dir

                # ruch samolotów w poziomie
                if self.enemy[i].ty == 10 or self.enemy[i].ty == 9:
                    if self.enemy[i].x > width and self.enemy[i].ty == 10:
                        self.enemy[i].x = 0
                    if self.enemy[i].x < 0 and self.enemy[i].ty == 9:
                        self.enemy[i].x = width
                    if not self.enemy[i].out and not self.plane.out:
                        self.enemy[i].x += self.enemy[i].dir

                # repozycjonowanie wrogów
                if self.enemy[i].y == screen_height - eny_box / 3:
                    self.enemy[i].y = 0
                    if self.base.y < self.enemy[i].y < self.base.y + 400:
                        self.enemy[i].out = True
                    else:
                        self.enemy[i].out = False

                    # losowanie typów wrogów i stacji paliw
                    enemys = [4, 6, 7, 8, 9, 10, 11]
                    rnd = random.randint(0, 6)
                    self.enemy[i].ty = enemys[rnd]
                    if rnd == 0 or rnd == 1:
                        self.enemy[i].w = 42
                        self.enemy[i].h = 30
                    elif rnd == 2 or rnd == 3:
                        self.enemy[i].w = 81
                        self.enemy[i].h = 24
                    elif rnd == 4 or rnd == 5:
                        self.enemy[i].w = 48
                        self.enemy[i].h = 18
                    elif rnd == 6:
                        self.enemy[i].w = 37
                        self.enemy[i].h = 72

                    # Generowanie losowych pozycji dla wrogów
                    pos = True
                    while pos:
                        self.enemy[i].x = random.randint(0, 8) * 84 + 23
                        pos = self.hitcortest(self.enemy[i], self.cor[2])

                    self.enemy[i].y = -eny_box / 3

                if -370 <= self.base.y < 50 and self.enemy[i].y == screen_height + eny_box / 2:
                    self.enemy[i].out = True

                if self.enemy[i].y == screen_height + eny_box / 2:
                    self.enemy[i].y = -eny_box / 2

            self.enemy[i].show()

        # Zużycie paliwa
        if not intro and mover:
            gazlev += 1
            if gazlev > 100:
                gazlev = 0
                gaz_level -= 5
            if gaz_level < 0:
                gaz_level = 0

        # Ostrzeżenie o niskim poziomie paliwa
        if gaz_level <= 70 and s_gaz_alert == "gaz_full":
            s_gaz_alert = "gaz_alert"
            self.gaz_alert.play(-1)
        if gaz_level <= 5 and gazlev > 80 and s_gaz_alert == "gaz_alert":
            s_gaz_alert = "gaz_end"
            self.gaz_alert.stop()
            self.gaz_end.play()

        if s_gaz_alert != "gaz_full" and gaz_level > 70:
            s_gaz_alert = "gaz_full"
            self.gaz_end.stop()
            self.gaz_alert.stop()

    def lands(self):
        # ruch bazy
        if game and not intro and not self.plane.t_expl:
            self.base.y += mover * vel_y

        for i in range(3):
            self.ilha[i].y = self.base.y - (2000+i*246)
            self.terra[i].y = self.base.y - (330+i*300)
            if intro:
                self.terra_intro.show()

            if self.terra[i].y < screen_height:
                self.terra[i].show()

            if self.ilha[i].y < screen_height:
                self.ilha[i].show()

        self.terra_intro.y = self.base.y + 210

        for i in range(3):
            # ruch domów i bazy w osi Y
            self.casa[i].y += mover * vel_y

            # losowe pozycjonowanie domów
            if self.casa[i].y == screen_height:
                self.casa[i].y = 0
                rnd_casa = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                random.shuffle(rnd_casa)  # tasowanie tablicy
                for j in range(0, 8):
                    self.casa[i].x = rnd_casa[j] * self.casa[i].w + 25
                    if self.hitcortest(self.casa[i], self.cor[3]) or self.pontes[2].t_expl or self.colidir(self.casa[i], self.pontes[0]) or self.colidir(self.casa[i], self.pontes[1]) or self.colidir(self.casa[i], self.pontes[2]):
                        self.casa[i].out = True
                    else:
                        self.casa[i].out = False
                        break

            if self.casa[i].y < screen_height:
                self.casa[i].show()

            # Mosty
            self.pontes[i].y = self.base.y + 164
            if -screen_height < self.base.y < screen_height:
                self.pontes[i].show()
        self.pontes[2].y = self.base.y + 169

        # Regeneracja mostu
        if self.base.y > screen_height and not intro:
            self.pontes[2].out = False

    def paint(self):
        pygame.display.update()
        # Rzeka
        if self.pontes[2].t_expl % 2:
            self.win.fill(self.cor[8])
        else:
            self.win.fill(self.cor[3])

        # Zwolnienie kontroli
        if not self.plane.out and not intro:
            self.control()

        self.tiro.show(self.plane.x + self.plane.w/2, self.plane.y + self.plane.h/2)

        # Tło
        self.win.fill(self.cor[2], rect=[0, 0, 20, height])
        self.win.fill(self.cor[2], rect=[width - 20, 0, 20, height])

        if -screen_height < self.base.y < screen_height:
            self.base.show()

        self.lands()
        self.inimigos()
        self.plane.show()

        # Panel
        self.win.fill(self.cor[7], rect=[0, screen_height, width, 130])
        self.win.fill(self.cor[14], rect=[0, height - 117, width, 112])

        # wskaźnik paliwa
        pygame.draw.rect(self.win, self.cor[7], [320, 515, 204, 44], 4)
        pygame.draw.rect(self.win, self.cor[7], [335, 515, 11, 13])
        pygame.draw.rect(self.win, self.cor[7], [422, 515, 5, 13])
        pygame.draw.rect(self.win, self.cor[7], [500, 515, 11, 13])

        self.textos()

        # Restartowanie bazy i wysp
        if self.ilha[2].y > screen_height:
            self.base.y = -400
            for i in range(3):
                self.terra[i].forma = random.randint(0, 7)
                self.ilha[i].forma = random.randint(0, 13)

    def textos(self):
        # wskaźnik
        font = pygame.font.SysFont("arial", 33)
        txt = font.render("E        " + chr(189) + "      F", 0, (0, 0, 0))
        self.win.blit(txt, (334, 524))
        pygame.draw.rect(self.win, self.cor[1], [335 + gaz_level, 529, 10, 27])

        # Życia
        if vidas:
            font = pygame.font.SysFont("cooper Black", 34)
            txt = font.render(str(vidas), 0, (232, 232, 74))
            self.win.blit(txt, (290, 554))

        # Punkty
        if pontos:
            font = pygame.font.SysFont("cooper Black", 34)
            txt = font.render(str(pontos), 0, (232, 232, 74))
            self.win.blit(txt, (450, 474))

        # Tekst
        if not game:
            font = pygame.font.SysFont("arial Black", 30)
            txt = font.render("Python", 0, (232, 232, 74))
            self.win.blit(txt, (364, 552))

    def control(self):
        global delay_y, speed, mover

        print(f"Sterowanie - Pozycja samolotu: ({self.plane.x}, {self.plane.y}), Gra: {game}, Intro: {intro}, Ruch: {mover}")

        if game and not intro:
            speed += 1
            if speed > delay_y:
                mover = True
                speed = 0
            else:
                mover = False

        self.plane.ty = 0
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.plane.x > 10:
            self.plane.x -= 1
            self.plane.ty = 1
        if key[K_RIGHT] and self.plane.x < 734:
            self.plane.x += 1
            self.plane.ty = 2

        if key[K_UP]:
            if delay_y > 0:
                self.voo0.stop()
                self.voo1.stop()
                self.voo2.play(-1)
            delay_y = 0
        elif key[K_DOWN]:
            if delay_y < 2:
                self.voo1.stop()
                self.voo2.stop()
                self.voo0.play(-1)
            delay_y = 2
        else:
            if delay_y != 1:
                self.voo0.stop()
                self.voo2.stop()
                self.voo1.play(-1)
            delay_y = 1

        if key[K_SPACE]:
            self.tiro.shoting = True
            if self.tiro.y == self.plane.y - 15:
                self.s_tiro.stop()
                self.s_tiro.play()

if __name__ == "__main__":
    game = Game()
    game.main_menu()
    pygame.quit()
