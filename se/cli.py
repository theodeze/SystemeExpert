import os
import sys
from se import BaseDeFaits, Fait, AnalyseurSyntaxique, BaseDeRegles, MoteurDInferance, Trace

class CLI:

    def __init__(self):
        self.basedefaits = BaseDeFaits()
        self.basederegles = BaseDeRegles()
        self.moteur = MoteurDInferance()

    def menu(self):
        try:
            cmd = ""
            print("Système Expert d'ordre 0+")
            print("Tapez \"aide\" pour plus d'informations.")
            while cmd != "quitter" and cmd != "exit":
                print(">>>", end=' ')
                cmd = input()
                if cmd.startswith("lire"):
                    nom_fichier = cmd.lstrip("lire").strip()
                    self.lire_fichier(nom_fichier)
                elif cmd.startswith("reinitialise"):
                    self.reinitialiser()
                elif cmd.startswith("trace"):
                    niveau = cmd.lstrip("trace").strip()
                    if "non" in niveau:
                        self.moteur.trace = Trace.NON
                        print("Trace " + self.moteur.trace.value)
                    elif "min" in niveau:
                        self.moteur.trace = Trace.MIN
                        print("Trace " + self.moteur.trace.value)
                    elif "oui" in niveau:
                        self.moteur.trace = Trace.OUI
                        print("Trace " + self.moteur.trace.value)
                    elif niveau == "":
                        print("Trace " + self.moteur.trace.value)
                    else:
                        print("ALERTE: Niveau trace non reconnus, valeur possible { oui, min, non }")
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
                    AnalyseurSyntaxique.analyse_ligne(cmd, self.basedefaits, self.basederegles)
        except KeyboardInterrupt:
            sys.exit(0)
    
    def aide(self):
        print("Liste des commandes :")
        print("\tlire <Nom fichier> : lire un fichier")
        print("\treinitialise : reinitialiser la Base de connaissance")
        print("\ttrace : affiche le niveau de trace")
        print("\ttrace <Niveau> : fixe le niveau de trace { oui, min, non }")
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
        return Fait(nom_fait, AnalyseurSyntaxique.analyse_valeur(valeur_fait))

    def chainage_avant(self):
        self.moteur.chainage_avant(self.basedefaits,self.basederegles,self.demande_fait())

    def chainage_arriere(self):
        self.moteur.chainage_arriere(self.basedefaits,self.basederegles,self.demande_fait(),None,None)

    def reinitialiser(self):
        self.basedefaits.faits = []
        self.basederegles.regles = []
        print("Base de connaissance réinitialisé")

    def lire_fichier(self, nom_fichier):
        if not os.path.isfile(nom_fichier) or not os.access(nom_fichier, os.R_OK):
            print("Le fichier {} n'existe pas".format(nom_fichier))
        else:
            nregles = len(self.basederegles.regles)
            nfaits = len(self.basedefaits.faits)
            AnalyseurSyntaxique.analyse_fichier(nom_fichier, self.basedefaits, self.basederegles)
            print("Ajout de {} faits et {} rêgles".format(len(self.basedefaits.faits)-nfaits, len(self.basederegles.regles)-nregles))


def main():
    cli = CLI()
    cli.menu()

if __name__ == '__main__':
    main()