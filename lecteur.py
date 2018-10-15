from basedefaits import Fait

class Lecteur:

    def __init__(self):
        self.clasf = 0

    def lire_fichier(self, basedefaits, base_regles):
        with open("fichier.txt") as fichier:
            l = 0
            nb_utiles = []
            for lignes in fichier:
                if l == 0:
                    nb_utiles=lignes.split(" ")
                    
                if l > 0 and l <= int(nb_utiles[0]):
                    string=lignes.split("\n")[0]
                    basedefaits.ajouter_fait(Fait(self.decoupageBaseFaits(string)[0],self.analyseType(self.decoupageBaseFaits(string)[1])))

                l +=1
                #if l > int(nb_utiles[0]):
                #    self.remplirTableau(base_regles,lignes.split("\n")[0])        
        fichier.close()

    def remplirTableau(self, tableau, string):
        return tableau.append(string)
        
    def analyseType(self, valeur):
        if (valeur.isdigit()):
            return int(valeur)
        elif (valeur=="True"):
            return True
        elif (valeur=="False"):
            return False
        else :
            return valeur

    def decoupageBaseFaits(self, string):
        return string.split("=")

    def decoupageBaseRegles(self, string):
        return string.split("")