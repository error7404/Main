#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import os
if os.getcwd()[-4:] != "Code":
    try:
        os.chdir("Code")
    except:
        raise SystemExit("pas dans le bon dossier")
    
from math import floor

import pygame
from Joueur import Joueur
from Lecteur_De_Matrice import Lecteur_De_Matrice
from Point import Point
from Fonction import *
from Selecteur_de_niveaux import *
from Menu import *
import time as ti;
import json

pygame.init()
icon = pygame.image.load("../Texture/Menu/Logo.png")
pygame.display.set_icon(icon)
if __name__ == '__main__' and not sys.argv[-1] == "--no_menu":
    menus()
time = 0

times = 0
fps = 0
imgnbr = 0

# Code RGB du noir et du blanc
BLUE = (60, 60, 255)
WHITE = (255, 255, 255)
screen_color = pygame.Color(0,0,0)
# Taille de l'écran
SIZE = (1280, 720)
# l'horloge est utilisée pour le contrôle de la vitesse de rafraîchissement de l’écran
clock = pygame.time.Clock()

# apparition du personnage
Sprite_Droite = pygame.image.load('../Texture/Joueur/Heros_vue_de_cote.png')
Sprite_Gauche = pygame.image.load('../Texture/Joueur/Heros_vue_de_cote_gauche.png')

Sprite_J1 = Sprite_Droite

# Création d'une fenêtre à la taille choisie
pygame.display.set_caption("Pixel Run")
screen = pygame.display.set_mode(SIZE)

winning = False

running = True

Level_actuelle = 4

mono = floor(ti.time())

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MC', 25)



while running:

    matrice = Charger_Level(Level_actuelle)
    J1 = Joueur(Point(128, 128), 0.04, Point(0, 0))
    if Level_actuelle == 2:
        J1 = Joueur(Point(64, 500), 0.04, Point(0, 0))
    # boucle tant que cette condition est vraie (running)
    while running:
        # récupère un morceaux de la colonne de la matrice dans lequelle le joueur est entrain de tomber
        tranche = [matrice[i][int(J1.Pied().x // 64)] for i in
                   range(int(J1.Pied().y // 64), int((J1.Pied().y + J1.Velocite.y) // 64 + 1))]
        # détermine si c'est un bloc plein ou pas (collision)
        if 0 in tranche:
            if J1.Velocite.y != 0:
                y_Block = tranche.index(0)
                J1.Velocite.y = ((J1.Pied().y // 64 + y_Block) * 64) - J1.Pied().y
        else:
            J1.Chute_Libre()
        if 3 in tranche:
            if J1.Velocite.y != 0:
                y_Block = tranche.index(3)
                J1.Velocite.y = ((J1.Pied().y // 64 + y_Block) * 64) - J1.Pied().y
                J1 = Joueur(Point(128, 128), 0.04)
        tranche_Haut = [matrice[i][int(J1.Tete().x // 64)] for i in
                        range(int(J1.Tete().y // 64), int((J1.Tete().y + J1.Velocite.y) // 64) - 1, -1)]
        if J1.Velocite.y < 0 and 0 in tranche_Haut:
            # J1.Velocite.y = 0
            y_Block = tranche_Haut.index(0)
            J1.Velocite.y = ((J1.Tete().y // 64 - y_Block + 1) * 64) - J1.Tete().y
        J1.Changer_Position()
        # si user ferme la fenetre
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_a] or keys[pygame.K_LEFT]:
                J1.Bouger_Joueur(Direction_Gauche=True)
                Sprite_J1 = Sprite_Gauche
            if keys[pygame.K_d]or keys[pygame.K_RIGHT]:
                J1.Bouger_Joueur(Direction_Gauche=False)
                Sprite_J1 = Sprite_Droite
            if keys[pygame.K_SPACE]:
                if 0 in tranche:
                    J1.Sauter()

            if keys[pygame.K_RETURN]:
                import restart
                pygame.quit()
                raise SystemExit()

            if not keys[pygame.K_q] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d] and not keys[pygame.K_LEFT] and not keys[pygame.K_a]:
                J1.Velocite.x = 0
            # que l'event est fermeture de la fenetre
            if event.type == pygame.QUIT:
                running = False
                print("Fermeture du jeu")
                pygame.quit()
        tranche_Gauche = [matrice[i][int(J1.collision_Haut_Gauche().x // 64):int(
            (J1.collision_Haut_Gauche().x + J1.Velocite.x) // 64) + 1] for i in
                          range(int(J1.collision_Haut_Gauche().y // 64), int(J1.collision_Bas_Gauche().y // 64) + 1)]
        if J1.Velocite.x < 0 and 0 in tableau_aplatir(tranche_Gauche):
            J1.Velocite.x = 0
        tranche_Droite = [matrice[i][int(J1.collision_Haut_Droite().x // 64):int(
            (J1.collision_Haut_Droite().x + J1.Velocite.x) // 64) + 1] for i in
                          range(int(J1.collision_Haut_Droite().y // 64), int(J1.collision_Bas_Droite().y // 64) + 1)]
        if J1.Velocite.x > 0 and 0 in tableau_aplatir(tranche_Droite):
            J1.Velocite.x = 0
        if J1.Velocite.x < 0 and 2 in tableau_aplatir(tranche_Gauche):
            running = False
            winning = True
        if J1.Velocite.x > 0 and 2 in tableau_aplatir(tranche_Droite):
            running = False
            winning = True
        # affichage de la matrice et du
        if screen_color.hsva[0]+1 < 360:
            screen_color.hsva =  (screen_color.hsva[0]+1,100,100,100)
        else:
            screen_color.hsva =  (0,100,100,100)
        screen.fill(screen_color) # pour ne pas avoir l'ecran RGB mettre une autre valeur a la place de screen_color
        Lecteur_De_Matrice(0, 20, 0, 20, matrice, screen)
        screen.blit(Sprite_J1, (int(J1.Position.x), int(J1.Position.y)))
        # --- ‘update’ l’écran avec le dessin des lignes
        if floor(ti.time()) == mono + 1:
            imgnbr = fps
            fps = 0
            mono = floor(ti.time())
            times = times + 1

        fps = fps + 1

        img = myfont.render('FPS : ' + str(imgnbr), True, (50, 50, 50))
        screen.blit(img, (75, 75))

        img = myfont.render('Temps : ' + str(times), True, (50, 50, 50))
        screen.blit(img, (75, 95))

        pygame.display.flip()
        # --- limité à 60 ‘cadres’ par seconde
        clock.tick(60)
        if time >= 10:
            # ferme la fenetre
            running = False
            # remet le joueur au point de départ
            # J1 = Joueur(Point(128,128),0.04)
    if winning:
        running = True
        winning = False
        Level_actuelle += 1
    #if Level_actuelle > 4:
    if not os.path.isfile(f"Level_{Level_actuelle}.json") and not os.path.isfile(f"Code/Level_{Level_actuelle}.json"):
        running = False
        winning = True
if winning:
    i = 0
    while i < 300:
        screen.fill(BLUE)
        screen.blit(pygame.image.load("../Texture/Menu/Win_screen.png"), (0, 0))

        myfont = pygame.font.SysFont('Comic Sans MC', 35)
        img = myfont.render('Temps : ' + str(times) + ' secondes', True, (50, 50, 50))
        screen.blit(img, (850, 305))

        try:
            with open('record.json') as json_file:
                data = json.load(json_file)
                record = data['record']
        except:
            record = -1

        if record > times or record == -1:
            with open('record.json', 'w') as outfile:
                outfile.write(json.dumps({"record":times}))
            record = times

        myfont = pygame.font.SysFont('Comic Sans MC', 35)
        img = myfont.render('Record : ' + str(record), True, (50, 50, 50))
        screen.blit(img, (885, 13))

        pygame.display.flip()
        i += 1
        clock.tick(60)


pygame.quit()
