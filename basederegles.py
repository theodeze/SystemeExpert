# coding=utf8
from enum import Enum, unique

from basedefaits import BaseDeFaits, Fait

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

    def ajouter(self, basedefaits):
        if self.operateur == Operateur.AFFECTATION:
            basedefaits.ajouter_fait(Fait(self.expression, self.value))


class Regle:

    def __init__(self):
        self.premisses = []
        self.conclusions = []
        self.est_desactive = False

    def __str__(self):
        chaine = ""
        premiere = True
        for proposition in self.premisses:
            if premiere:
                chaine += "SI    " + str(proposition) + "\n"
                premiere = False
            else:
                chaine += "ET    " + str(proposition) + "\n"
        premiere = True
        chaine += "ALORS "
        for proposition in self.conclusions:
            if premiere:
                chaine += str(proposition)
                premiere = False
            else:
                chaine += " ET " + str(proposition)
        chaine += "\n"
        return chaine

    def ajouter_premisse(self, proposition):
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition doit être une proposition")
        self.premisses.append(proposition)

    def ajouter_conclusion(self, proposition):
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition doit être une proposition")
        self.conclusions.append(proposition)

    def applicable(self, basedefaits):
        applicable = True
        if self.est_desactive:
            applicable = False
        for proposition in self.premisses:
            applicable = applicable and proposition.valeur(basedefaits)
        return applicable
    
    def appliquer(self, basedefaits):
        if not self.est_desactive:
            for proposition in self.conclusions:
                proposition.ajouter(basedefaits)
    
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
        chaine += "============="
        return chaine

    def ajouter_regle(self, regle):
        if not isinstance(regle, Regle):
            raise TypeError("regle doit être une regle")
        self.regles.append(regle)

    def applicable(self, basedefaits):
        applicable = False
        for regle in self.regles:
            applicable = applicable or regle.applicable(basedefaits)
        return applicable            
    
    def selection(self, basedefaits):
        for regle in self.regles:
            if regle.applicable(basedefaits):
                return regle
        return None

    def activer_tous(self):
        for regle in self.regles:
            regle.activer()