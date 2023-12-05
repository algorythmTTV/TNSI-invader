import pygame # importation de la librairie pygame
import sys # pour fermer correctement l'application
import space

### INITIALISATION ###
# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders") 
# chargement de l image de fond
fond = pygame.image.load('fichiers/documents pour eleves/background.png')

# creation du joueur
player = space.Joueur()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée
            print("Quelqu'un a appuyé sur une touche !")
            if event.key == pygame.K_LEFT: # si la touche est la fleche gauche
                player.sens = "gauche" 
                print("j'ai appuyé sur la fleche gauche")
            if event.key == pygame.K_RIGHT: # si la touche est la fleche droite
                player.sens = "droite" 
                print("j'ai appuyé sur la fleche droite")
        if event.type == pygame.KEYUP:
            player.sens=0
            print("Plus de touche appuyée")
            
    ### Actualisation de la scene ###
    # deplacement des objets
    player.deplacer()
    # dessins des objets        
    screen.blit(player.image,(player.position,500))

    pygame.display.update() # pour mettre à jour l'écran
