import pygame  # necessaire pour charger les images et les sons
import random as r


class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self,
                 sens=0,
                 image=pygame.image.load("fichiers/documents pour eleves/vaisseau.png"),
                 position=400,
                 vitesse=1,
                 score=0):
        self.sens=sens
        self.image=image
        self.position=position
        self.vitesse=vitesse
        self.score=score

    def deplacer(self):
        if self.sens=="gauche" and self.position>0:
            self.position-=self.vitesse
        elif self.sens=="droite" and self.position<736:
            self.position+=self.vitesse
    
    def marquer(self):
        pass




class Balle():
    def __init__(self,
                 joueur,
                 hauteur=500,
                 image=pygame.image.load("fichiers/documents pour eleves/balle.png"),
                 etat="chargee"):
        self.joueur=joueur
        self.depart=self.joueur.position+19
        self.hauteur=hauteur
        self.image=image
        self.etat=etat
        self.image.set_alpha(0)

    def bouger(self):
        if self.etat=="chargee":
            self.depart=self.joueur.position+18
        else:
            self.hauteur-=1
            self.image.set_alpha(255)
            if self.hauteur<0:
                self.etat="chargee"
                self.hauteur=500
                self.image.set_alpha(0)
    
    def toucher(self,ennemi):
        if self.hauteur==ennemi.hauteur:
            return True
        return False



class Ennemi:
    NbEnnemis=15
    types={1:["invader1",
              "fichiers/documents pour eleves/invader1.png",
              1],
              2:["invader2",
                 "fichiers/documents pour eleves/invader2.png",
                 2]}

    def __init__(self,
                 depart=r.randint(10,726),
                 type=types[r.randint(1,2)],
                 hauteur=64):
        self.depart=depart
        self.type=type[0]
        self.image=pygame.image.load(type[1])
        self.vitesse=type[2]
        self.hauteur=hauteur

    def avancer(self):
        self.hauteur+=self.vitesse

    def disparaitre(self):
        pass