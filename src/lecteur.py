import re
from .base import Fait, Proposition, Operateur
from .basederegles import Regle

class Lecteur:

    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self.clasf = 0

    def lire_fichier(self, basedefaits, basederegles):
        with open(self.nom_fichier) as fichier:
            for ligne in fichier:
                Lecteur.lire_ligne(ligne.split("\n")[0], basedefaits, basederegles)
        fichier.close()
        
    @staticmethod
    def lire_ligne(ligne, basedefaits, basederegles):
        if ":=" in ligne:
            conclusions = Lecteur.decoupageBaseRegles(ligne)[0]
            premises = Lecteur.decoupageBaseRegles(ligne)[1]
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
            if Lecteur.decoupageBaseFaits(ligne)[0].strip() == "":
                print("ALERTE: un fait ne peut pas avoir un nom vide\n" + ligne)
                return
            if Lecteur.decoupageBaseFaits(ligne)[1].strip() == "":
                print("ALERTE: un fait ne peut être égale à une chaîne vide\n" + ligne)
                return
            try:
                basedefaits.ajouter_fait(Fait(Lecteur.analyse_chaine(Lecteur.decoupageBaseFaits(ligne)[0]), 
                    Lecteur.analyse_chaine(Lecteur.decoupageBaseFaits(ligne)[1])))
            except Exception as e:
                print("ALERTE: {}\n{}".format(e, ligne))
        elif ligne != "" and ligne[0] != "#":
            print("ALERTE: ligne non reconnus\n" + ligne)

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

    @staticmethod
    def decoupageBaseFaits(chaine):
        return chaine.split("=")

    @staticmethod
    def decoupageBaseRegles(chaine):
        return chaine.split(":=")