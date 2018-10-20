import re
from core.base import Fait, Proposition, Operateur
from core.basederegles import Regle

class Lecteur:

    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self.clasf = 0

    def lire_fichier(self, basedefaits, basederegles):
        with open(self.nom_fichier) as fichier:
            for ligne in fichier:

                if ":=" in ligne:
                    string = ligne.split("\n")[0]
                    conclusions = self.decoupageBaseRegles(string)[0]
                    premises = self.decoupageBaseRegles(string)[1]
                    regle = Regle()
                    for conclusion in conclusions.split("&"):
                        regle.ajouter_conclusion(Fait(Lecteur.analyse_chaine(conclusion.split("=")[0]), 
                            Lecteur.analyse_chaine(conclusion.split("=")[1])))
                    for premise in re.split(r'(&+|\|\|+)',premises):
                        if "&" in premise:
                            regle.ajouter_operateurs(Operateur.ET)
                        elif "||" in premise:
                            regle.ajouter_operateurs(Operateur.OU)
                        elif "==" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split("==")[0]), 
                                Operateur.EGALITE, 
                                Lecteur.analyse_chaine(premise.split("==")[1])))
                        elif "!=" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split("!=")[0]), 
                                Operateur.INEGALITE, 
                                Lecteur.analyse_chaine(premise.split("!=")[1])))
                        elif "<=" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split("<=")[0]), 
                                Operateur.INFERIORITEOUEGALITE, 
                                Lecteur.analyse_chaine(premise.split("<=")[1])))
                        elif "<" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split("<")[0]), 
                                Operateur.INFERIORITE, 
                                Lecteur.analyse_chaine(premise.split("<")[1])))
                        elif ">=" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split(">=")[0]), 
                                Operateur.SUPERIORITEOUEGALITE, 
                                Lecteur.analyse_chaine(premise.split(">=")[1])))
                        elif ">" in premise:
                            regle.ajouter_premisse(Proposition(Lecteur.analyse_chaine(premise.split(">")[0]), 
                                Operateur.SUPERIORITE, 
                                Lecteur.analyse_chaine(premise.split(">")[1])))
                    basederegles.ajouter_regle(regle) 

                elif "=" in ligne:
                    string = ligne.split("\n")[0]
                    basedefaits.ajouter_fait(Fait(Lecteur.analyse_chaine(self.decoupageBaseFaits(string)[0]), 
                        Lecteur.analyse_chaine(self.decoupageBaseFaits(string)[1])))

                elif ligne != "\n" and ligne[0] != "#":
                    print("WARNING: ligne non reconnus\n" + ligne.split("\n")[0])
        fichier.close()
        
    @staticmethod
    def analyse_chaine(chaine):
        chaine = chaine.strip()
        if chaine.isdigit():
            return float(chaine)
        elif chaine == "True" or chaine == "Vrai":
            return True
        elif chaine=="False" or chaine == "Faux":
            return False
        else:
            return chaine

    def decoupageBaseFaits(self, chaine):
        return chaine.split("=")

    def decoupageBaseRegles(self, chaine):
        return chaine.split(":=")