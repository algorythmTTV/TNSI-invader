import pygame
from pygame import mixer as mx

listeMusiques = [
    "fichiers/musique/musique_1.mp3",
    "fichiers/musique/musique_2.mp3",
    "fichiers/musique/musique_3.mp3",
    "fichiers/musique/musique_4.mp3",
    "fichiers/musique/musique_5.mp3"
]

def fin():
    mx.music.stop()
    mx.Sound("fichiers/sons/game_over.wav")
    son.set_volume(0.2)
    son.play()
    son = mx.Sound("fichiers/sons/dead.wav")
    son.play()