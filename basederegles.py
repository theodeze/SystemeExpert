# coding=utf8
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
        self.est_desactive = False

    def __str__(self):
        chaine = ""
        premiere = True
        for proposition in self.premisse:
            if premiere:
                chaine += "SI    " + str(proposition) + "\n"
                premiere = False
            else:
                chaine += "ET    " + str(proposition) + "\n"
        chaine += "ALORS " + str(self.conclusion) + "\n"
        return chaine

    def ajouter_premisse(self, proposition):
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition doit être une proposition")
        self.premisse.append(proposition)

    def applicable(self, basedefaits):
        applicable = True
        if self.desactiver:
            applicable = False
        for proposition in self.premisse:
            applicable = applicable and proposition.valeur(basedefaits)
        return applicable
    
    def appliquer(self, basedefaits):
        if self.conclusion.applicable(basedefaits) and not self.est_desactive:
            self.conclusion.ajouter(basedefaits)
    
    def desactiver(self):
        self.est_desactive = True

    def activer(self):
        self.est_desactive = False


class BaseDeRegles: 

    def __init__(self):
        self.regles = []
    
    def __str__(self):
        chaine = "============= "
        chaine += "Base de rêgle\n"
        for regle in self.regles:
            chaine += str(regle)
        chaine += "=============\n"
        return chaine

    def ajouter_regle(self, regle):
        if not isinstance(regle, Regle):
            raise TypeError("regle doit être une regle")
        self.regles.append(regle)

    def applicable(self, basedefaits):
        applicable = True
        for regle in self.regles:
            applicable = applicable and regle.applicable(basedefaits)
        return applicable            
    
    def selection(self, basedefaits):
        for regle in self.regles:
            if regle.applicable(basedefaits):
                return regle
        return None

    def activer_tous(self):
        for regle in self.regles:
            regle.activer()