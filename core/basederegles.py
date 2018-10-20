from .base import Fait, Proposition, Operateur
from .basedefaits import BaseDeFaits

class Regle:

    def __init__(self):
        self.premisses = []
        self.conclusions = []
        self.operateurs = []
        self.est_desactive = False

    def __str__(self):
        chaine = ""
        premiere = True
        index = 0
        for proposition in self.premisses:
            if premiere:
                chaine += str(proposition)
                premiere = False
            else:
                chaine += " " + self.operateurs[index].value + " " + str(proposition)
                index += 1
        premiere = True
        chaine += " → "
        for proposition in self.conclusions:
            if premiere:
                chaine += str(proposition)
                premiere = False
            else:
                chaine += " ∧ " + str(proposition)
        return chaine

    def ajouter_premisse(self, proposition):
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition doit être une proposition")
        self.premisses.append(proposition)

    def ajouter_operateurs(self, operateur):
        if not isinstance(operateur, Operateur):
            raise TypeError("operateur doit être une Operateur")
        self.operateurs.append(operateur)

    def liste_premisses(self):
        return self.premisses

    def ajouter_conclusion(self, fait):
        if not isinstance(fait, Fait):
            raise TypeError("fait doit être un Fait")
        self.conclusions.append(fait)

    def liste_conclusions(self):
        return self.conclusions

    def contient_conclusion(self, fait):
        if isinstance(fait, Fait):
            for conclusion in self.conclusions:
                if Fait.egale(conclusion, fait):
                    return True
        if isinstance(fait, Proposition):
            for conclusion in self.conclusions:
                if fait.operateur == Operateur.EGALITE:
                    if Fait.egale(Fait(fait.expression, fait.value), conclusion):
                        return True
                elif fait.operateur == Operateur.INEGALITE:
                    if Fait.inegale(Fait(fait.expression, fait.value), conclusion):
                        return True
                elif fait.operateur == Operateur.SUPERIORITE:
                    if Fait.inferieur(Fait(fait.expression, fait.value), conclusion):
                        return True
                elif fait.operateur == Operateur.SUPERIORITEOUEGALITE:
                    if Fait.inferieur_egale(Fait(fait.expression, fait.value), conclusion):
                        return True
                elif fait.operateur == Operateur.INFERIORITE:
                    if Fait.superieur(Fait(fait.expression, fait.value), conclusion):
                        return True
                elif fait.operateur == Operateur.INFERIORITEOUEGALITE:
                    if Fait.superieur_egale(Fait(fait.expression, fait.value), conclusion):
                        return True
        return False

    def applicable(self, basedefaits):
        if self.est_desactive:
            return False
        applicable = True
        index = -1
        for proposition in self.premisses:
            if index == -1:
                applicable = proposition.valeur(basedefaits)
                index +=1
            elif self.operateurs[index] == Operateur.ET:
                applicable = applicable and proposition.valeur(basedefaits)
                index +=1
            elif self.operateurs[index] == Operateur.OU:
                applicable = applicable or proposition.valeur(basedefaits)
                index +=1
        return applicable
    
    def appliquer(self, basedefaits):
        if not self.est_desactive:
            for fait in self.conclusions:
                basedefaits.ajouter_fait(fait)
    
    def desactiver(self):
        self.est_desactive = True

    def activer(self):
        self.est_desactive = False


class BaseDeRegles: 

    def __init__(self):
        self.regles = []
    
    def __str__(self):
        chaine =  "======== Base de Rêgle ========\n"
        for regle in self.regles:
            chaine += str(regle) + "\n"
        chaine += "==============================="
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

    def list_regles_ayant_conclusion(self, conclusion):
        ensemble_regle = []
        for regle in self.regles:
            if regle.contient_conclusion(conclusion):
                ensemble_regle.append(regle)
        return ensemble_regle

    def activer_tous(self):
        for regle in self.regles:
            regle.activer()