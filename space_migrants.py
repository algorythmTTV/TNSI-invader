import pygame
import space
import sys
import random as r

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")

player = space.Joueur()
score_precedent=player.score
vg_precedente=0
sc=space.Nombre(player.score,50)
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

# listeObstacles=[]

fond_menu=pygame.image.load("fichiers/fond/fond.png").convert_alpha()
screen.blit(fond_menu, [0,0])
pygame.display.update()
son=pygame.mixer.Sound("fichiers/sons/start.wav")
son.play()
commence = False
while not commence:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            commence = True
            son=pygame.mixer.Sound("fichiers/sons/shoot.wav")
            son.play()
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
                    running=False
        if balle.hauteur < 0:
            balle.hauteur = player.hauteur
    else:
        vague_passee.play()
        space.Ennemi.vague += 1
        space.Ennemi.NbEnnemis = space.Ennemi.vagues[space.Ennemi.vague]
        for indice in range(space.Ennemi.NbEnnemis):
            vaisseau = space.Ennemi()
            listeEnnemis.append(vaisseau)

    for f in listeFond:
        f.avancer()
        screen.blit(f.image,[f.largeur,f.hauteur])
    player.deplacer()
    balle.bouger()

    if vg_precedente!=space.Ennemi.vague:
        vg=space.Nombre(space.Ennemi.vague,50)
        for i in range(len(vg.images)):
            screen.blit(vg.images[i],[i*50,1030])
    else:
        for i in range(vg.images):
            screen.blit(vg.images[i],[i*50,1030])

    if score_precedent!=player.score:
        sc=space.Nombre(player.score,50)
        for i in range(len(sc.images)):
            screen.blit(sc.images[i],[i*50,0])
    else:
        for i in range(len(sc.images)):
            screen.blit(sc.images[i],[i*50,0])

    screen.blit(balle.image, [balle.depart, balle.hauteur])
    screen.blit(player.image, [player.position, player.hauteur])

    for extra in listeEnnemis:
        extra.avancer()
        screen.blit(extra.image, [extra.depart, round(extra.hauteur)])
    
    # for i in range((space.Ennemi.vague+1)):
    #     obst=space.Obstacle()
    #     listeObstacles.append(obst)
    # 
    # for obstacle in listeObstacles:
    #     obstacle.avancer()
    #     if obstacle.hauteur>=1080:
    #         listeObstacles.remove(obstacle)
    #     else:
    #         obstacle.collision(player)
    #         screen.blit(obstacle.image_stable, [obstacle.depart, obstacle.hauteur])

    score_precedent=player.score
    pygame.display.update()


pygame.mixer.music.stop()
son=pygame.mixer.Sound("fichiers/sons/game_over.wav")
son.set_volume(0.2)
son.play()
son=pygame.mixer.Sound("fichiers/sons/dead.wav")
son.play()
fin=pygame.image.load("fichiers/fond/fin.png").convert_alpha()
for i in range(256):
    fin.set_alpha(i)
    screen.blit(fin, [0,0])
    pygame.display.update()
screen.blit(fin, [0,0])
pygame.display.update()
exit = False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            exit = True
