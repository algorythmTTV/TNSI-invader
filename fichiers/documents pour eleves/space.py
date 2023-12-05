import pygame  # necessaire pour charger les images et les sons


class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self,sens=0,image=pygame.image.load("fichiers/documents pour eleves/vaisseau.png"),position=400,vitesse=1):
        self.sens=sens
        self.image=image
        self.position=position
        self.vitesse=vitesse

    def deplacer(self):
        if self.sens=="gauche" and self.position>0:
            self.position-=self.vitesse
        elif self.sens=="droite" and self.position<736:
            self.position+=self.vitesse



class Balle():
    def __init__(self,joueur,hauteur=500,image=pygame.image.load("fichiers/documents pour eleves/balle.png"),etat="chargee"):
        self.joueur=joueur
        self.depart=self.joueur.position+19
        self.hauteur=hauteur
        self.image=image
        self.etat=etat
        image.set_alpha(0)

    def bouger(self):
        self.depart=self.joueur.position+18

    def tirer(self):
        pass