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

    @staticmethod
    def valuer_chaine(chaine, basedefaits):
        if isinstance(chaine, bool):
            return chaine
        if isinstance(chaine, float):
            return chaine
        if chaine.startswith('"') and chaine.endswith('"'):
            return chaine
        return basedefaits.valeur_fait(self.expression)

    @staticmethod
    def est_fait(chaine):
        if isinstance(chaine, bool):
            return False
        if isinstance(chaine, float):
            return False
        if chaine.startswith('"') and chaine.endswith('"'):
            return False
        return True

    def inverser(self):
        tmp = self.expression
        self.expression = self.value
        self.value = tmp
        if self.operateur == Operateur.INFERIORITE:
            self.operateur = Operateur.SUPERIORITE
        elif self.operateur == Operateur.INFERIORITEOUEGALITE:
            self.operateur = Operateur.SUPERIORITEOUEGALITE
        elif self.operateur == Operateur.SUPERIORITE:
            self.operateur = Operateur.INFERIORITE
        elif self.operateur == Operateur.SUPERIORITEOUEGALITE:
            self.operateur = Operateur.INFERIORITEOUEGALITE

    def en_fait(self, basedefaits):
        if Proposition.est_fait(self.expression) and Proposition.est_fait(self.value):
            if basedefaits.valeur_fait(self.expression) != None:
                return Fait(self.value, basedefaits.valeur_fait(self.expression))
            elif basedefaits.valeur_fait(self.value) != None:
                self.inverser()
                return Fait(self.value, basedefaits.valeur_fait(self.expression))
        elif Proposition.est_fait(self.expression) and not Proposition.est_fait(self.value):
            return Fait(self.expression, self.value)
        elif not Proposition.est_fait(self.expression) and Proposition.est_fait(self.value):
            self.inverser()
            return Fait(self.expression, self.value)
        elif not Proposition.est_fait(self.expression) and not Proposition.est_fait(self.value):
            return self.valeur(basedefaits)
        return None
    
    def valeur(self, basedefaits):
        value = False
        value_fait = Proposition.valuer_chaine(self.expression, basedefaits)
        if value_fait == None:
            return False
        valeur_droite = Proposition.valuer_chaine(self.value, basedefaits)
        if valeur_droite == None:
            return False
        if self.operateur == Operateur.EGALITE:
            value = value_fait == valeur_droite
        elif self.operateur == Operateur.INEGALITE:
            value = value_fait != valeur_droite
        elif self.operateur == Operateur.SUPERIORITE:
            value = value_fait > valeur_droite
        elif self.operateur == Operateur.SUPERIORITEOUEGALITE:
            value = value_fait >= valeur_droite
        elif self.operateur == Operateur.INFERIORITE:
            value = value_fait < valeur_droite
        elif self.operateur == Operateur.INFERIORITEOUEGALITE:
            value = value_fait <= valeur_droite
        return value
