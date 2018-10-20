from enum import Enum, unique

class Fait:

    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

    def __str__(self):
        if self.valeur == True:
            return "{}".format(self.nom)
        if self.valeur == False:
            return "¬{}".format(self.nom)
        return "{} = {}".format(self.nom, self.valeur)
    
    @staticmethod
    def egale(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur == fait2.valeur
        
    @staticmethod
    def inegale(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur != fait2.valeur

    @staticmethod
    def inferieur(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur > fait2.valeur

    @staticmethod
    def inferieur_egale(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur >= fait2.valeur

    @staticmethod
    def superieur(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur < fait2.valeur

    @staticmethod
    def superieur_egale(fait1, fait2):
        return fait1.nom == fait2.nom and fait1.valeur <= fait2.valeur


@unique
class Operateur(Enum):
    EGALITE = "=="
    INEGALITE = "!="
    SUPERIORITE = ">"
    SUPERIORITEOUEGALITE = ">="
    INFERIORITE = "<"
    INFERIORITEOUEGALITE = "<="
    ET = "∧"
    OU = "∨"


class Proposition:
    
    def __init__(self, expression, operateur, value):
        if not isinstance(expression, str):
            raise TypeError("expression doit être une string")
        if not isinstance(operateur, Operateur):
            raise TypeError("operateur doit être un operateur")
        self.expression = expression
        self.operateur = operateur
        self.value = value

    def __str__(self):
        if self.value == True:
            return "{}".format(self.expression)
        if self.value == False:
            return "¬{}".format(self.expression)
        return "{} {} {}".format(self.expression, self.operateur.value, self.value)

    @staticmethod
    def egale(proposition1, proposition2):
        return proposition1.expression == proposition2.expression and proposition1.value == proposition2.value

    def valeur(self, basedefaits):
        value = False
        value_fait = basedefaits.valeur_fait(self.expression)
        if basedefaits.valeur_fait(self.expression) == None:
            return False
        if self.operateur == Operateur.EGALITE:
            value = value_fait == self.value
        elif self.operateur == Operateur.INEGALITE:
            value = value_fait != self.value
        elif self.operateur == Operateur.SUPERIORITE:
            value = value_fait > self.value
        elif self.operateur == Operateur.SUPERIORITEOUEGALITE:
            value = value_fait >= self.value
        elif self.operateur == Operateur.INFERIORITE:
            value = value_fait < self.value
        elif self.operateur == Operateur.INFERIORITEOUEGALITE:
            value = value_fait <= self.value
        return value
