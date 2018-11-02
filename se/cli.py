import os
import sys
from se import Log, BaseDeFaits, Fait, AnalyseurSyntaxique, BaseDeRegles, MoteurDInferance, Trace, SelectionRegle

class CLI:

    def __init__(self):
        self.basedefaits = BaseDeFaits()
        self.basederegles = BaseDeRegles()
        self.moteur = MoteurDInferance()

    def menu(self):
        Log.init()
        try:
            cmd = ""
            print("Système Expert d'ordre 0+")
            print("Tapez \"aide\" pour plus d'informations.")
            while cmd != "quitter" and cmd != "exit":
                print(">>>", end=' ')
                self.commande(input())
            Log.remove_log()
        except KeyboardInterrupt:
            sys.exit(0)
    
    def commande(self, cmd):
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
        elif cmd.startswith("regle"):
            niveau = cmd.lstrip("regle").strip()
            if "plus" in niveau:
                self.moteur.selection_regle = SelectionRegle.PLUS
                print("Choix de règle par " + self.moteur.selection_regle.value)
            elif "complexe" in niveau:
                self.moteur.selection_regle = SelectionRegle.COMPLEXE
                print("Choix de règle par " + self.moteur.selection_regle.value)
            elif "premiere" in niveau:
                self.moteur.selection_regle = SelectionRegle.PREMIERE
                print("Choix de règle par " + self.moteur.selection_regle.value)
            elif niveau == "":
                print("Règle choisi par " + self.moteur.selection_regle.value)
            else:
                print("ALERTE: Type règle non reconnus, valeur possible { premiere, complexe, plus }")
        elif cmd.startswith("afficher"):
            affiche = cmd.lstrip("afficher").strip()
            if "faits" in affiche:
                self.afficher_faits()
            elif "regles" in affiche:
                self.afficher_regles()
            elif affiche == "":
                self.afficher_faits()
                self.afficher_regles()
            else:
                print("ALERTE: Type règle non reconnus, valeur possible { faits, regles }")
        elif cmd.startswith("log"):
            Log.print()
        elif cmd == "av":
            self.chainage_avant()
        elif cmd == "ar":
            self.chainage_arriere()
        elif cmd == "aide" or cmd == "help":
            self.aide()
        elif cmd != "quitter" and cmd != "exit" and cmd != "":
            AnalyseurSyntaxique.analyse_ligne(cmd, self.basedefaits, self.basederegles)

    def aide(self):
        print("Liste des commandes :")
        print("\tlire nom_du_fichier.txt : Charge un fichier")
        print("\ttrace [non|min|oui] : Modifie le type d'affichage lors du chainage")
        print("\tregle [plus|complexe|premiere] : Modifie le type de selection des rêgles")
        print("\tafficher [faits|regles] : Affiche les faits et/ou les rêgles")
        print("\taide : Affiche l'aide")
        print("\treinitialise : Reinitialiser la Base de connaissance")
        print("\tquitter : quitter")
        print("\tav : chainage avant")
        print("\tar : chainage arriere")
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


def main_cli():
    cli = CLI()
    cli.menu()

if __name__ == '__main__':
    main_cli()