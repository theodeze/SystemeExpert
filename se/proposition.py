from se import Operateur, Fait, AnalyseurSimple

class Proposition:

    def __init__(self, expression_gauche, operateur, expression_droite):
        self.expression_gauche = expression_gauche
        self.operateur = operateur
        self.expression_droite = expression_droite
    
    def __str__(self):
        if self.operateur == Operateur.EGALITE:
            if isinstance(self.expression_gauche, bool) and self.expression_gauche:
                return "{}".format(self.expression_droite)
            elif isinstance(self.expression_droite, bool) and self.expression_droite:
                return "{}".format(self.expression_gauche)
            elif isinstance(self.expression_gauche, bool) and not self.expression_gauche:
                return "¬{}".format(self.expression_droite)
            elif isinstance(self.expression_droite, bool) and not self.expression_droite:
                return "¬{}".format(self.expression_gauche)
        if self.operateur == Operateur.INEGALITE:
            if isinstance(self.expression_gauche, bool) and self.expression_gauche:
                return "¬{}".format(self.expression_droite)
            elif isinstance(self.expression_droite, bool) and self.expression_droite:
                return "¬{}".format(self.expression_gauche)
            elif isinstance(self.expression_gauche, bool) and not self.expression_gauche:
                return "{}".format(self.expression_droite)
            elif isinstance(self.expression_droite, bool) and not self.expression_droite:
                return "{}".format(self.expression_gauche)
        return "{} {} {}".format(self.expression_gauche, self.operateur.value, self.expression_droite)

    def en_fait(self, basedefaits):
        if AnalyseurSimple.est_fait(self.expression_gauche) and AnalyseurSimple.est_fait(self.expression_droite):
            valeur_gauche = AnalyseurSimple.valuer_expression(self.expression_gauche, basedefaits)
            valeur_droite = AnalyseurSimple.valuer_expression(self.expression_droite, basedefaits)
            if valeur_gauche != None and valeur_droite != None:
                return self.valeur(basedefaits)
            elif valeur_gauche == None and valeur_droite != None:
                return Fait(self.expression_gauche, valeur_droite)
            elif valeur_gauche != None and valeur_droite == None:
                return Fait(self.expression_droite, valeur_gauche)
        elif not AnalyseurSimple.est_fait(self.expression_gauche) and AnalyseurSimple.est_fait(self.expression_droite):
            return Fait(self.expression_droite, self.expression_gauche)
        elif AnalyseurSimple.est_fait(self.expression_gauche) and not AnalyseurSimple.est_fait(self.expression_droite):
            return Fait(self.expression_gauche, self.expression_droite)
        elif not AnalyseurSimple.est_fait(self.expression_gauche) and not AnalyseurSimple.est_fait(self.expression_droite):
            return self.valeur(basedefaits)
        return False

    def valeur(self, basedefaits):
        valeur = False
        valeur_gauche = AnalyseurSimple.valuer_expression(self.expression_gauche, basedefaits)
        if valeur_gauche == None:
            return False
        valeur_droite = AnalyseurSimple.valuer_expression(self.expression_droite, basedefaits)
        if valeur_droite == None:
            return False
        if self.operateur == Operateur.EGALITE:
            valeur = valeur_gauche == valeur_droite
        elif self.operateur == Operateur.INEGALITE:
            valeur = valeur_gauche != valeur_droite
        elif self.operateur == Operateur.SUPERIORITE:
            valeur = valeur_gauche > valeur_droite
        elif self.operateur == Operateur.SUPERIORITEOUEGALITE:
            valeur = valeur_gauche >= valeur_droite
        elif self.operateur == Operateur.INFERIORITE:
            valeur = valeur_gauche < valeur_droite
        elif self.operateur == Operateur.INFERIORITEOUEGALITE:
            valeur = valeur_gauche <= valeur_droite
        return valeur