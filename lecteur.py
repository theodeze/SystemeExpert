from basedefaits import Fait
from basederegles import Regle, Proposition, Operateur

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
                        regle.ajouter_conclusion(Proposition(conclusion.split("=")[0], Operateur.AFFECTATION, self.analyse_chaine(conclusion.split("=")[1])))
                    for premise in premises.split("&"):
                        if "==" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("==")[0], Operateur.EGALITE, self.analyse_chaine(premise.split("==")[1])))
                        elif "!=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("!=")[0], Operateur.INEGALITE, self.analyse_chaine(premise.split("!=")[1])))
                        elif "<=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("<=")[0], Operateur.INFERIORITEOUEGALITE, self.analyse_chaine(premise.split("<=")[1])))
                        elif "<" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("<")[0], Operateur.INFERIORITE, self.analyse_chaine(premise.split("<")[1])))
                        elif ">=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split(">=")[0], Operateur.SUPERIORITEOUEGALITE, self.analyse_chaine(premise.split(">=")[1])))
                        elif ">" in premise:
                            regle.ajouter_premisse(Proposition(premise.split(">")[0], Operateur.SUPERIORITE, self.analyse_chaine(premise.split(">")[1])))
                    basederegles.ajouter_regle(regle) 

                elif "=" in ligne:
                    string = ligne.split("\n")[0]
                    basedefaits.ajouter_fait(Fait(self.decoupageBaseFaits(string)[0],self.analyse_chaine(self.decoupageBaseFaits(string)[1])))

                elif ligne != "\n" and ligne[0] != "#":
                    print("WARNING: ligne non reconnus\n" + ligne.split("\n")[0])

        fichier.close()
        
    def analyse_chaine(self, chaine):
        chaine = chaine.strip();
        if chaine.isdigit():
            return float(chaine)
        elif chaine == "True" or chaine == "Vrais":
            return True
        elif chaine=="False" or chaine == "Faux":
            return False
        else:
            return chaine

    def decoupageBaseFaits(self, chaine):
        return chaine.split("=")

    def decoupageBaseRegles(self, chaine):
        return chaine.split(":=")