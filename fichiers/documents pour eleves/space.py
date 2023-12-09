import pygame  # necessaire pour charger les images et les sons
import random as r


class Joueur: # classe pour créer le vaisseau du joueur
    def __init__(self,
                 sens=0,
                 image=pygame.image.load("fichiers/images/Ship_1_A_Small.png"),
                 position=510,
                 vitesse=4,
                 score=0,
                 hauteur=870,
                 vie=3):
        self.sens=sens
        self.image=image
        self.position=position
        self.vitesse=vitesse
        self.score=score
        self.hauteur=hauteur
        self.vie=vie

    def deplacer(self):
        if self.sens=="gauche" and self.position>0:
            self.position-=self.vitesse
        elif self.sens=="droite" and self.position<1856:
            self.position+=self.vitesse
        elif self.sens=="haut" and self.hauteur>840:
            self.hauteur-=self.vitesse
        elif self.sens=="bas" and self.hauteur<960:
            self.hauteur+=self.vitesse
    
    def marquer(self):
        self.score+=1
        print(self.score)




class Balle:
    max=3
    def __init__(self,
                 joueur,
                 image=pygame.image.load("fichiers/images/Missile_A_Small.png"),
                 etat="chargee"):
        self.joueur=joueur
        self.depart=self.joueur.position+19
        self.hauteur=joueur.hauteur
        self.image=image
        self.etat=etat
        self.image.set_alpha(0)

    def bouger(self):
        if self.etat=="chargee":
            self.depart=self.joueur.position+18
            self.hauteur=self.joueur.hauteur
        else:
            self.hauteur-=4
            self.image.set_alpha(255)
            self.etat="tiree"
            if self.hauteur<0:
                self.etat="chargee"
                self.hauteur=self.joueur.hauteur
                self.image.set_alpha(0)
    
    def toucher(self, ennemi):
        if (
            self.etat == "tiree"
            and ennemi.depart <= self.depart <= ennemi.depart + ennemi.image.get_width()
            and ennemi.hauteur <= self.hauteur <= ennemi.hauteur + ennemi.image.get_height()
        ):
            self.etat = "chargee"
            print("touché")
            self.hauteur = self.joueur.hauteur
            self.image.set_alpha(0)
            return True

        return False



class Ennemi:
    vague=0
    vagues=[1,2,4,8,15]
    NbEnnemis=vagues[vague]
    types={1:["invader1",
              "fichiers/images/Enemy_1_A_Small.png",
              1.5],
              2:["invader2",
                 "fichiers/images/Enemy_2_A_Small.png",
                 2.2]}

    def __init__(self,
                 types=types):
        self.depart=r.randint(10,1846)
        self.type=types[r.randint(1,2)]
        image=pygame.image.load(self.type[1])
        self.image=image
        self.vitesse=self.type[2]
        self.hauteur=r.randint(-500,0)

    def avancer(self):
        self.hauteur+=self.vitesse

class Fond:
    layers=[{"image":pygame.image.load("fichiers/fond/layer_1.png"),"vitesse":1},
            {"image":pygame.image.load("fichiers/fond/layer_2.png"),"vitesse":2},
            {"image":pygame.image.load("fichiers/fond/layer_3.png"),"vitesse":3}]
    
    def __init__(self,num,layers=layers,hauteur=0,largeur=180):
        image=layers[num]["image"]
        self.image=pygame.transform.rotozoom(image,0,2)
        self.vitesse=layers[num]["vitesse"]
        self.hauteur=hauteur
        self.largeur=largeur
    
    def avancer(self):
        self.hauteur+=self.vitesse