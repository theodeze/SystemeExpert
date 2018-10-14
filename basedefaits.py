class BaseDeFaits:
    
    def __init__(self):
        self.faits = {}

    def __str__(self):
        str = "========== Base de Faits =========="
        for cle, valeur in self.faits.items():
            str += "{}: {}\n".format(cle, valeur)
        return str

    def ajouter_fait(self, cle, valeur):
        self.faits[cle] = valeur

    def valeur_fait(self, cle):
        if cle not in self.faits:
            self.ajouter_fait(cle, None)
        return self.faits[cle]