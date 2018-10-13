
#    une base de faits
#    une base de règles
#    un moteur d'inférence.

class baseDeFaits:
    
    def __init__(self):
        self.faits = {}

    def __str__(self):
        str = ""
        for cle, valeur in self.faits.items():
            str += "{}: {}\n".format(cle, valeur)
        return str

    def ajouter_fait(self, cle, valeur):
        self.faits[cle] = valeur

    def valeur_fait(self, cle):
        if cle not in self.faits:
            self.ajouter_fait(cle, None)
        return self.faits[cle]


base_test = baseDeFaits()
base_test.ajouter_fait("Grand", True)
print(base_test)
base_test.ajouter_fait("Taille", 108)
print(base_test)