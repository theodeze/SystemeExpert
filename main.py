
from systemeexpert.basedefaits import *
from systemeexpert.basederegles import *
from systemeexpert.moteurdinference import *

#    une base de faits
#    une base de règles
#    un moteur d'inférence.

class regle:

    def __init__(self):
        self.premisse = []
        self.conclusion = 5


class baseDeRegles:

    def __init__(self):
        self.regles = []
    


base_test = BaseDeFaits()
base_test.ajouter_fait("Grand", True)
print(base_test)
base_test.ajouter_fait("Taille", 108)
print(base_test)