import os
import os.path

from core.basedefaits import BaseDeFaits, Fait
from core.basederegles import BaseDeRegles
from core.moteurdinference import MoteurDInferance
from lecteur import Lecteur

def main():
    print("Nom fichier ?")
    nom_fichier = input()
    if not os.path.isfile(nom_fichier) or not os.access(nom_fichier, os.R_OK):
        print("\x1B[38;31mLe fichier n'existe pas\x1B[0m")
        return

    basedefaits = BaseDeFaits()
    basederegles = BaseDeRegles()
    moteur = MoteurDInferance(True)
    lecteur = Lecteur(nom_fichier)
    lecteur.lire_fichier(basedefaits,basederegles)

    print(basedefaits)
    print(basederegles)

    print("Nom du fait recherché ?")
    nom_fait = input()
    print("Valeur du fait ?")
    valeur_fait = input()
    fait = Fait(nom_fait,Lecteur.analyse_chaine(valeur_fait))

    type_chainage = "" 
    while type_chainage != "0" and type_chainage != "1":
        print("Type de chainage (0: Avant, 1: Arriere) ?")
        type_chainage = input()

    if type_chainage == "0":
        moteur.chainage_avant(basedefaits,basederegles,fait)
    else:
        moteur.chainage_arriere(basedefaits,basederegles,fait,None,None)


if __name__ == '__main__':
    main()