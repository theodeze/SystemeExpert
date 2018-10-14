from enum import Enum, unique

from basedefaits import *

@unique
class Operateur(Enum):
    AFFECTATION = "="
    EGALITE = "=="
    INEGALITE = "!="
    SUPERIORITE = ">"
    SUPERIORITEOUEGALITE = ">="
    INFERIORITE = "<"
    INFERIORITEOUEGALITE = "<="


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
        return "{} {} {}".format(self.expression, self.operateur.value, self.value)

    def valeur(self, basedefaits):
        value = False
        if self.operateur == Operateur.EGALITE:
            value = basedefaits.valeur_fait(self.expression) == self.value
        elif self.operateur == Operateur.INEGALITE:
            value = basedefaits.valeur_fait(self.expression) != self.value
        elif self.operateur == Operateur.SUPERIORITE:
            value = basedefaits.valeur_fait(self.expression) > self.value
        elif self.operateur == Operateur.SUPERIORITEOUEGALITE:
            value = basedefaits.valeur_fait(self.expression) >= self.value
        elif self.operateur == Operateur.INFERIORITE:
            value = basedefaits.valeur_fait(self.expression) < self.value
        elif self.operateur == Operateur.INFERIORITEOUEGALITE:
            value = basedefaits.valeur_fait(self.expression) <= self.value
        return value

    def ajouter(self, basedefaits):
        if self.operateur == Operateur.AFFECTATION:
            basedefaits.ajouter_fait(self.expression, self.value)


class Regle:

    def __init__(self, conclusion):
        self.premisse = []
        self.conclusion = conclusion

    def __str__(self):
        str = ""
        premiere = True
        for proposition in self.premisse:
            if premiere:
                str += "SI    " + proposition + "\n"
                premiere = False
            else:
                str += "ET    " + proposition + "\n"
        str += "ALORS " + self.conclusion

    def ajouter_premisse(self, proposition):
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition doit être une proposition")
        self.premisse.append(proposition)

    def applicable(self, basedefaits):
        applicable = True
        for proposition in self.premisse:
            applicable = applicable and proposition.valeur(basedefaits)
        return applicable
    
    def appliquer(self, basedefaits):
        if self.conclusion.applicable(basedefaits):
            self.conclusion.ajouter(basedefaits)
