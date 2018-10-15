class Fait:

    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

    def __str__(self):
        return "{} = {}".format(self.nom, self.valeur)


class BaseDeFaits:
    
    def __init__(self):
        self.faits = []

    def __str__(self):
        chaine = "============= "
        chaine += "Base de Faits\n"
        for fait in self.faits:
            chaine += str(fait) + "\n"
        chaine += "=============\n"
        return chaine

    def contient(self, fait_a_verifier):
        for fait in self.faits:
            if fait == fait_a_verifier:
                return True
        return False

    def ajouter_fait(self, fait_a_ajouter):
        for fait in self.faits:
            if fait.nom == fait_a_ajouter.nom:
                if fait.valeur == None:
                    fait.valeur = fait_a_ajouter.valeur
                    return
                elif fait.valeur == fait_a_ajouter.valeur:
                    raise Exception("Base de Faits inconsitante")
        self.faits.append(fait_a_ajouter)

    def valeur_fait(self, nom):
        for fait in self.faits:
            if fait.nom == nom:
                return fait.valeur
        self.ajouter_fait(Fait(nom, None))
        return None