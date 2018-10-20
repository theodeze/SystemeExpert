import os
import os.path
import sys

from basedefaits import BaseDeFaits, Fait
from basederegles import BaseDeRegles
from lecteur import Lecteur
from moteurdinference import MoteurDInferance

# from moteurdinference import *

#    une base de faits
#    une base de règles
#    un moteur d'inférence.


basedefaits = BaseDeFaits()
basederegles = BaseDeRegles()

print("Nom fichier ?")
nom_fichier = input()
if not os.path.isfile(nom_fichier) or not os.access(nom_fichier, os.R_OK):
    print("\x1B[38;31mLe fichier n'existe pas\x1B[0m")
    sys.exit()
lecteur = Lecteur(nom_fichier)
lecteur.lire_fichier(basedefaits,basederegles)



#basedefaits.ajouter_fait(Fait("Taille de Thomas", 175))
#basedefaits.ajouter_fait(Fait("Taille de Gidéone", 169))
#basedefaits.ajouter_fait(Fait("Grand", True))
#regle1 = Regle(Proposition("Grand", Operateur.AFFECTATION, True))
#regle1.ajouter_premisse(Proposition("Taille de Thomas", Operateur.SUPERIORITE, 150))
#regle1.ajouter_premisse(Proposition("Taille de Gidéon", Operateur.SUPERIORITE, 150))
#basederegles.ajouter_regle(regle1)

#if(basederegles.applicable(basedefaits)):
#    regle = basederegles.selection(basedefaits)
#    regle.appliquer(basedefaits)

print(basedefaits)
print(basederegles)

moteur = MoteurDInferance(True)

moteur.chainage_avant(basedefaits,basederegles,Fait("H",True))
#print(moteur.chainage_arriere(basedefaits,basederegles,Fait("H",True),None))

print(basedefaits)