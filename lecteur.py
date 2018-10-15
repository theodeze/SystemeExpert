# coding=utf8

class Lecteur:

    def __init__(self):
        self.clasf = 0

    def lire_fichier(self, base_connaissances, base_regles):
        with open(document) as fichier:
            l = 0
            nb_utiles = []
            for lignes in fichier:
                if l == 0:
                    nb_utiles=lignes.split(" ")
                    
                if l>0 and l <= int(nb_utiles[0]):
                    string=lignes.split("\n")[0]
                    basetdefait.ajouter_fait(Fait(decoupageBaseFaits(string)[0],analyseType(decoupageBaseFaits(string)[1]))

                if l >int(nb_utiles[0]):
                    remplirTableau(base_regles,lignes.split("\n")[0])        
        fichier.close()
    
    
def remplirTableau(self, tableau, string):
    return tableau.append(string)
    
def analyseType(self, valeur):
    if (valeur.isdigit()):
        return double(valeur)
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