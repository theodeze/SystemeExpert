from se import Log, Operateur, Fait, AnalyseurSimple

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

    def __eq__(self, proposition):
        return (self.expression_droite == proposition.expression_droite 
            and self.expression_gauche == proposition.expression_gauche
            and self.operateur == proposition.operateur) or (self.expression_droite == proposition.expression_gauche 
            and self.expression_gauche == proposition.expression_droite
            and self.operateur == Proposition.inv_operateur(proposition.operateur))

    def __ne__(self, proposition):
        return not (self.expression_droite == proposition.expression_droite 
            and self.expression_gauche == proposition.expression_gauche
            and self.operateur == proposition.operateur) or (self.expression_droite == proposition.expression_gauche 
            and self.expression_gauche == proposition.expression_droite
            and self.operateur == Proposition.inv_operateur(proposition.operateur))

    @staticmethod
    def inv_operateur(operateur):
        if operateur == Operateur.INFERIORITE:
            return Operateur.SUPERIORITE
        elif operateur == Operateur.INFERIORITEOUEGALITE:
            return Operateur.SUPERIORITEOUEGALITE
        elif operateur == Operateur.SUPERIORITE:
            return Operateur.INFERIORITE
        elif operateur == Operateur.SUPERIORITEOUEGALITE:
            return Operateur.INFERIORITEOUEGALITE
        else:
            return operateur

    def quel_operateur(self, basedefaits):
        if AnalyseurSimple.est_fait(self.expression_gauche) and AnalyseurSimple.est_fait(self.expression_droite):
            valeur_gauche = AnalyseurSimple.valuer_expression(self.expression_gauche, basedefaits)
            valeur_droite = AnalyseurSimple.valuer_expression(self.expression_droite, basedefaits)
            if valeur_gauche != None and valeur_droite != None:
                return self.operateur
            elif valeur_gauche == None and valeur_droite != None:
                return self.operateur
            elif valeur_gauche != None and valeur_droite == None:
                return Proposition.inv_operateur(self.operateur)
        elif not AnalyseurSimple.est_fait(self.expression_gauche) and AnalyseurSimple.est_fait(self.expression_droite):
            return Proposition.inv_operateur(self.operateur)
        elif AnalyseurSimple.est_fait(self.expression_gauche) and not AnalyseurSimple.est_fait(self.expression_droite):
            return self.operateur
        elif not AnalyseurSimple.est_fait(self.expression_gauche) and not AnalyseurSimple.est_fait(self.expression_droite):
            return self.operateur
        return self.operateur

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
        Log.warning("Transformation impossible car les deux valeurs sont inconnus")
        Log.warning("Il est possible qu'il faille relancer un chaînage")
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