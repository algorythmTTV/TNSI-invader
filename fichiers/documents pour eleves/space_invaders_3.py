import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders") 
# chargement de l'image de fond
#fond = pygame.image.load('fichiers/documents pour eleves/background.png')

# creation du joueur
player = space.Joueur()
# creation de la balle
balles=[]
for i in range(space.Balle.max):
    balle=space.Balle
    balle.etat="chargee"
    balles.append(balle)
# creation des ennemis
listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.fill((0,0,0))

    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.sens = "gauche" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.sens = "droite" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_UP:
                player.sens="haut"
            if event.key == pygame.K_DOWN:
                player.sens="bas"
            if event.key == pygame.K_SPACE : # espace pour tirer
                balles[0].etat="tiree"
        if event.type == pygame.KEYUP:
            player.sens=0

    ### Actualisation de la scene ###
    # Gestions des collisions
    if len(listeEnnemis)>0:
        for ennemi in listeEnnemis:
            if balles[0].toucher(ennemi):
                listeEnnemis.remove(ennemi)
                balles.pop(0)
                balles.append(space.Balle)
                player.marquer()
            elif ennemi.hauteur>1020:
                listeEnnemis.remove(ennemi)
                player.vie-=1
                if player.vie<=0:
                    print("Perdu!")
                    running=False
                    sys.exit()
        if balles[0].hauteur<0:
            balles.pop(1)
            balles.append(space.Balle)
    else:
        space.Ennemi.vague+=1
        space.Ennemi.NbEnnemis=space.Ennemi.vagues[space.Ennemi.vague]
        print("vague:",space.Ennemi.vague+1)
        for indice in range(space.Ennemi.NbEnnemis):
            vaisseau = space.Ennemi()
            listeEnnemis.append(vaisseau)
    # deplacement des objets
    player.deplacer()
    balles[0].bouger()
    # dessins des objets
    screen.blit(balles[0].image,[balles[0].depart,balles[0].hauteur]) # appel de la fonction qui dessine le vaisseau du joueur        
    screen.blit(player.image,[player.position,player.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
    # screen.blit(pygame.image.load("fichiers/documents pour eleves/coeur.png"),[0,0])
    # les ennemis
    for extra in listeEnnemis:
        extra.avancer()
        screen.blit(extra.image,[extra.depart, round(extra.hauteur)]) # appel de la fonction qui dessine le vaisseau du joueur
    pygame.display.update() # pour ajouter tout changement à l'écran
