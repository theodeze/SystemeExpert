import os
import os.path

from .basedefaits import BaseDeFaits, Fait
from .basederegles import BaseDeRegles
from .moteurdinference import MoteurDInferance
from .lecteur import Lecteur

class Interface:

    def __init__(self):
        self.basedefaits = BaseDeFaits()
        self.basederegles = BaseDeRegles()
        self.moteur = MoteurDInferance(True)

    def demarrer(self):
        cmd = ""
        print("Tapez \"aide\" pour plus d'informations.")
        while cmd != "quitter" and cmd != "exit":
            print(">>>", end=' ')
            cmd = input()
            if cmd == "0":
                self.lire_fichier()
            elif cmd == "1":
                self.afficher_faits()
            elif cmd == "2":
                self.afficher_regles()
            elif cmd == "3":
                self.chainage_avant()
            elif cmd == "4":
                self.chainage_arriere()
            elif cmd == "aide" or cmd == "help":
                self.aide()
            elif cmd != "quitter" and cmd != "exit" and cmd != "":
                Lecteur.lire_ligne(cmd, self.basedefaits, self.basederegles)
    
    def aide(self):
        print("Liste des commandes :")
        print("\t0 : lire un fichier")
        print("\t1 : afficher la base de faits")
        print("\t2 : afficher la base de regles")
        print("\t3 : chainage avant")
        print("\t4 : chainage arriere")
        print("\taide : afficher l'aide")
        print("\tquitter : quitter")
        print("Exemple:")
        print("\tA = Vrai : Ajout d'un fait")
        print("\tA = Vrai := B == Vrai & C == Faux : Ajout d'une regle")

    def afficher_regles(self):
        print(self.basederegles)

    def afficher_faits(self):
        print(self.basedefaits)

    def demande_fait(self):
        print("Nom du fait ?", end=' ')
        nom_fait = input()
        print("Valeur du fait ?", end=' ')
        valeur_fait = input()
        return Fait(nom_fait,Lecteur.analyse_chaine(valeur_fait))

    def chainage_avant(self):
        self.moteur.chainage_avant(self.basedefaits,self.basederegles,self.demande_fait())

    def chainage_arriere(self):
        self.moteur.chainage_arriere(self.basedefaits,self.basederegles,self.demande_fait(),None,None)

    def lire_fichier(self):
        nregles = len(self.basederegles.regles)
        nfaits = len(self.basedefaits.faits)
        nom_fichier = ""
        fichier_existe = False 
        print("Entrez le nom du fichier (a pour annuler)")
        while not fichier_existe and nom_fichier != "a":
            nom_fichier = input()
            if nom_fichier == "a":
                return
            if not os.path.isfile(nom_fichier) or not os.access(nom_fichier, os.R_OK):
                fichier_existe = False
            else:
                fichier_existe = True
            if not fichier_existe:
                CURSOR_UP_ONE = '\x1b[1A'
                ERASE_LINE = '\x1b[2K'
                print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
                print("\x1B[38;31mLe fichier n'existe pas\x1B[0m")
        lecteur = Lecteur(nom_fichier)
        lecteur.lire_fichier(self.basedefaits, self.basederegles)
        print("Ajout de {} faits et {} rêgles".format(len(self.basedefaits.faits)-nfaits, len(self.basederegles.regles)-nregles))


def main():
    interface = Interface()
    interface.demarrer()


if __name__ == '__main__':
    main()