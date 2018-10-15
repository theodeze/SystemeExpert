class Fait:

    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

    def __str__(self):
        return"{}: {}\n".format(self.nom, self.valeur)


class BaseDeFaits:
    
    def __init__(self):
        self.faits = []

    def __str__(self):
        str = "=============\n"
        str += "Base de Faits\n"
        for fait in self.faits:
            str + fait + "\n"
        str += "=============\n"
        return str

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
                else:
                    raise Exception("Base de Faits inconsitante")
        self.faits.append(fait_a_ajouter)

    def valeur_fait(self, nom):
        for fait in self.faits:
            if fait.nom == nom:
                return fait.valeur
        self.ajouter_fait(Fait(nom, None))
        return None