from basedefaits import Fait
from basederegles import Regle, Proposition, Operateur

class Lecteur:

    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self.clasf = 0

    def lire_fichier(self, basedefaits, basederegles):
        with open(self.nom_fichier) as fichier:
            l = 0
            for lignes in fichier:

                if ":=" in lignes:
                    string = lignes.split("\n")[0]
                    conclusions = self.decoupageBaseRegles(string)[0]
                    premises = self.decoupageBaseRegles(string)[1]
                    regle = Regle()
                    for conclusion in conclusions.split("&"):
                        regle.ajouter_conclusion(Proposition(conclusion, Operateur.AFFECTATION, True))
                    for premise in premises.split("&"):
                        if "==" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("==")[0], Operateur.EGALITE, self.analyseType(premise.split("==")[1])))
                        elif "!=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("!=")[0], Operateur.INEGALITE, self.analyseType(premise.split("!=")[1])))
                        elif "<=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("<=")[0], Operateur.INFERIORITEOUEGALITE, self.analyseType(premise.split("<=")[1])))
                        elif "<" in premise:
                            regle.ajouter_premisse(Proposition(premise.split("<")[0], Operateur.INFERIORITE, self.analyseType(premise.split("<")[1])))
                        elif ">=" in premise:
                            regle.ajouter_premisse(Proposition(premise.split(">=")[0], Operateur.SUPERIORITEOUEGALITE, self.analyseType(premise.split(">=")[1])))
                        elif ">" in premise:
                            regle.ajouter_premisse(Proposition(premise.split(">")[0], Operateur.SUPERIORITE, self.analyseType(premise.split(">")[1])))
                    basederegles.ajouter_regle(regle) 

                else:
                    string = lignes.split("\n")[0]
                    basedefaits.ajouter_fait(Fait(self.decoupageBaseFaits(string)[0],self.analyseType(self.decoupageBaseFaits(string)[1])))

                l +=1
        fichier.close()

    def remplirTableau(self, tableau, string):
        return tableau.append(string)
        
    def analyseType(self, valeur):
        if valeur.isdigit():
            return int(valeur)
        elif valeur=="True":
            return True
        elif valeur=="False":
            return False
        else :
            return valeur

    def decoupageBaseFaits(self, string):
        return string.split("=")

    def decoupageBaseRegles(self, string):
        return string.split(":=")