import pygame
import space
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")

player = space.Joueur()
balle = space.Balle(player)

listeFond=[]
for i in range(3):
    fond=space.Fond(i)
    listeFond.append(fond)

listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)

commence = False
while commence == False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            screen.fill((0, 0, 0))
            commence = True

running = True

while running:
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
                listeEnnemis.remove(ennemi)
                player.marquer()
            elif ennemi.hauteur > 1020:
                listeEnnemis.remove(ennemi)
                player.vie -= 1
                if player.vie <= 0:
                    print("Perdu!")
                    running = False
                    sys.exit()
        if balle.hauteur < 0:
            balle.hauteur = player.hauteur
    else:
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
