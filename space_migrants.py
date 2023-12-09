import pygame
import space
import sys
import random as r

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")

player = space.Joueur()
balle = space.Balle(player)

listeMusiques=["fichiers/musique/musique_1.mp3",
               "fichiers/musique/musique_2.mp3",
               "fichiers/musique/musique_3.mp3",
               "fichiers/musique/musique_4.mp3",
               "fichiers/musique/musique_5.mp3"]

vague_passee=pygame.mixer.Sound("fichiers/sons/vague_passee.wav")

listeFond=[]
for i in range(3):
    fond=space.Fond(i)
    listeFond.append(fond)

listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)


fond_menu=pygame.image.load("fichiers/fond/fond.png").convert_alpha()
screen.blit(fond_menu, [0,0])
pygame.display.update()
commence = False
while not commence:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            commence = True
screen.fill((0, 0, 0))

running = True

while running:
    if not pygame.mixer.music.get_busy():
        musique=r.choice(listeMusiques)
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
                balle.etat = "tiree"
        if event.type == pygame.KEYUP:
            player.sens = 0

    if len(listeEnnemis) > 0:
        for ennemi in listeEnnemis:
            if balle.toucher(ennemi):
                son=pygame.mixer.Sound("fichiers/sons/explosion.wav")
                son.play()
                ennemi.mort=True
                ennemi.explosion()
            elif ennemi.mort:
                ennemi.explosion()
                if ennemi.alpha<=0:
                    listeEnnemis.remove(ennemi)
                    player.marquer()
            elif ennemi.hauteur > 1080:
                listeEnnemis.remove(ennemi)
                player.vie -= 1
                if player.vie <= 0:
                    print("Perdu!")
                    running = False
                    sys.exit()
        if balle.hauteur < 0:
            balle.hauteur = player.hauteur
    else:
        vague_passee.play()
        space.Ennemi.vague += 1
        space.Ennemi.NbEnnemis = space.Ennemi.vagues[space.Ennemi.vague]
        print("vague:", space.Ennemi.vague + 1)
        for indice in range(space.Ennemi.NbEnnemis):
            vaisseau = space.Ennemi()
            listeEnnemis.append(vaisseau)

    for f in listeFond:
        f.avancer()
        screen.blit(f.image,[f.largeur,f.hauteur])
    player.deplacer()
    balle.bouger()

    

    screen.blit(balle.image, [balle.depart, balle.hauteur])
    screen.blit(player.image, [player.position, player.hauteur])

    for extra in listeEnnemis:
        extra.avancer()
        screen.blit(extra.image, [extra.depart, round(extra.hauteur)])

    pygame.display.update()
