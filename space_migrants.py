import pygame
import space
import sys
import random as r
import json

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")

player = space.Joueur()
score_precedent = player.score
vg_precedente = 0
sc = space.Nombre(player.score, 50)
balles=[]
for i in range(2):
    balle = space.Balle_A(player)
    balles.append(balle)

with open("fichiers/sauvegardes/save.json", "r") as fichier:
    donnees = json.load(fichier)
    print(donnees)
sc_save_last = space.Nombre(donnees["score"], 50)
sc_save_best = space.Nombre(donnees["best"], 50)

image_missile=pygame.image.load("fichiers/images/player/Missile_A_Small.png").convert_alpha()
image_missile2=pygame.image.load("fichiers/images/player/Missile_A_Small.png").convert_alpha()
image_missile2.set_alpha(100)

listeTextes = [
    pygame.transform.smoothscale(pygame.image.load("fichiers/images/text/score.png").convert_alpha(), (200, 200)),
    pygame.transform.smoothscale(pygame.image.load("fichiers/images/text/vague.png").convert_alpha(), (200, 200)),
    pygame.transform.smoothscale(pygame.image.load("fichiers/images/text/last.png").convert_alpha(), (200, 200)),
    pygame.transform.smoothscale(pygame.image.load("fichiers/images/text/best.png").convert_alpha(), (200, 200))
]

listeMusiques = [
    "fichiers/musique/musique_1.mp3",
    "fichiers/musique/musique_2.mp3",
    "fichiers/musique/musique_3.mp3",
    "fichiers/musique/musique_4.mp3",
    "fichiers/musique/musique_5.mp3"
]

vague_passee = pygame.mixer.Sound("fichiers/sons/vague_passee.wav")

listeFond = [space.Fond(i) for i in range(3)]

listeEnnemis = [space.Ennemi() for _ in range(space.Ennemi.NbEnnemis)]

fond_menu = pygame.image.load("fichiers/fond/fond.png").convert_alpha()
screen.blit(fond_menu, [0, 0])
pygame.display.update()
son = pygame.mixer.Sound("fichiers/sons/start.wav")
son.play()
commence = False
while not commence:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            commence = True
            son = pygame.mixer.Sound("fichiers/sons/shoot.wav")
            son.play()
screen.fill((0, 0, 0))

running = True

while running:
    if not pygame.mixer.music.get_busy():
        musique = r.choice(listeMusiques)
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.sens = "gauche"
            if event.key == pygame.K_RIGHT:
                player.sens = "droite"
            if event.key == pygame.K_UP:
                player.sens = "haut"
            if event.key == pygame.K_DOWN:
                player.sens = "bas"
            if event.key == pygame.K_SPACE:
                for balle in balles:
                    if balle.etat=="chargee":
                        balle.etat="tiree"
                        break
        if event.type == pygame.KEYUP:
            player.sens = 0

    if len(listeEnnemis) > 0:
        for ennemi in listeEnnemis:
            if balles[0].toucher(ennemi) or balles[1].toucher(ennemi):
                son = pygame.mixer.Sound("fichiers/sons/explosion.wav")
                son.play()
                ennemi.mort = True
                ennemi.explosion()
            elif ennemi.mort:
                ennemi.explosion()
                if ennemi.alpha <= 0:
                    listeEnnemis.remove(ennemi)
                    player.marquer()
            elif ennemi.hauteur > 1080:
                listeEnnemis.remove(ennemi)
                player.vie -= 1
                if player.vie <= 0:
                    running = False
    else:
        vague_passee.play()
        space.Ennemi.vague += 1
        space.Ennemi.NbEnnemis = space.Ennemi.vagues[space.Ennemi.vague]
        listeEnnemis.extend([space.Ennemi() for _ in range(space.Ennemi.NbEnnemis)])

    for f in listeFond:
        f.avancer()
        screen.blit(f.image, [f.largeur, f.hauteur])
    player.deplacer()
    for balle in balles:
        balle.bouger()
        if balle.hauteur < 0:
            balle.hauteur=player.hauteur

    screen.blit(listeTextes[1], [0, 955])
    if vg_precedente != space.Ennemi.vague:
        vg = space.Nombre(space.Ennemi.vague, 50)
        for i in range(len(vg.images)):
            screen.blit(vg.images[i], [(i + 5) * 35, 1030])
    else:
        for i in range(vg.images):
            screen.blit(vg.images[i], [(i + 5) * 35, 1030])

    screen.blit(listeTextes[0], [0, -75])
    if score_precedent != player.score:
        sc = space.Nombre(player.score, 50)
        for i in range(len(sc.images)):
            screen.blit(sc.images[i], [(i + 5) * 35, 0])
    else:
        for i in range(len(sc.images)):
            screen.blit(sc.images[i], [(i + 5) * 35, 0])

    screen.blit(listeTextes[2], [1920 - (len(sc_save_last.images) * 35) - 150, -75])
    for i in range(len(sc_save_last.images)):
        screen.blit(sc_save_last.images[i], [(1920 - (len(sc_save_last.images) * 35) + (i * 35)), 0])

    screen.blit(listeTextes[3], [1920 - (len(sc_save_best.images) * 35) - 150, 955])
    for i in range(len(sc_save_best.images)):
        screen.blit(sc_save_best.images[i], [(1920 - (len(sc_save_best.images) * 35) + (i * 35)), 1030])

    screen.blit(balles[0].image, [balles[0].depart, balles[0].hauteur])
    screen.blit(balles[1].image, [balles[1].depart, balles[1].hauteur])
    screen.blit(player.image, [player.position, player.hauteur])

    for extra in listeEnnemis:
        extra.avancer()
        screen.blit(extra.image, [extra.depart, round(extra.hauteur)])

    if sc_save_best.nb < player.score:
        sc_save_best = space.Nombre(player.score, 50)

    if balles[0].etat=="chargee" and balles[1].etat=="chargee":
        screen.blit(image_missile,[896,1016])
        screen.blit(image_missile,[960,1016])
    elif (balles[0].etat=="chargee" and balles[1].etat=="tiree") or (balles[1].etat=="chargee" and balles[0].etat=="tiree"):
        screen.blit(image_missile,[896,1016])
        screen.blit(image_missile2,[960,1016])
    else:
        screen.blit(image_missile2,[896,1016])
        screen.blit(image_missile2,[960,1016]) 

    score_precedent = player.score
    pygame.display.update()

save_last = {"score": player.score, "best": sc_save_best.nb}
with open("fichiers/sauvegardes/save.json", "w") as fichier:
    json.dump(save_last, fichier)

pygame.mixer.music.stop()
son = pygame.mixer.Sound("fichiers/sons/game_over.wav")
son.set_volume(0.2)
son.play()
son = pygame.mixer.Sound("fichiers/sons/dead.wav")
son.play()
fin = pygame.image.load("fichiers/fond/fin.png").convert_alpha()
for i in range(256):
    fin.set_alpha(i)
    screen.blit(fin, [0, 0])
    pygame.display.update()
screen.blit(fin, [0, 0])
pygame.display.update()
exit = False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            exit = True
