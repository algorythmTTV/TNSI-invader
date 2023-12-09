import pygame
import random as r



class Joueur:
    def __init__(self,
                 sens=0,
                 position=896,
                 vitesse=4,
                 score=0,
                 hauteur=870,
                 vie=3):
        self.sens = sens
        self.image = pygame.image.load("fichiers/images/Ship_1_A_Small.png").convert_alpha()
        self.position = position
        self.vitesse = vitesse
        self.score = score
        self.hauteur = hauteur
        self.vie = vie

    def deplacer(self):
        if self.sens=="gauche" and self.position>610:
            self.position-=self.vitesse
        elif self.sens=="droite" and self.position<1182:
            self.position+=self.vitesse
        elif self.sens=="haut" and self.hauteur>840:
            self.hauteur-=self.vitesse
        elif self.sens=="bas" and self.hauteur<960:
            self.hauteur+=self.vitesse
    
    def marquer(self):
        self.score+=1
        print(self.score)




class Balle:
    max = 3
    def __init__(self, joueur, etat="chargee"):
        self.joueur = joueur
        self.depart = self.joueur.position + 19
        self.hauteur = joueur.hauteur
        self.image = pygame.image.load("fichiers/images/Missile_A_Small.png").convert_alpha()
        self.etat = etat
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
            and ennemi.depart - 64 <= self.depart <= ennemi.depart + ennemi.image.get_width()
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
        self.depart=r.randint(610,1182)
        self.type=types[r.randint(1,2)]
        image=pygame.image.load(self.type[1]).convert_alpha()
        self.image=image
        self.vitesse=self.type[2]
        self.hauteur=r.randint(-500,-100)

    def avancer(self):
        self.hauteur+=self.vitesse


class Fond:
    layers = [
        {"image": "fichiers/fond/layer_1.png", "vitesse": 1},
        {"image": "fichiers/fond/layer_2.png", "vitesse": 2},
        {"image": "fichiers/fond/layer_3.png", "vitesse": 3}
    ]

    def __init__(self, num, hauteur=-10440, largeur=600):
        layer_info = self.layers[num]
        image_path = layer_info["image"]
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.vitesse = layer_info["vitesse"]
        self.hauteur = hauteur
        self.largeur = largeur

    def avancer(self):
        if self.hauteur==0:
            self.hauteur=-10440
        else:
            self.hauteur += self.vitesse