from se import Fait, Proposition, Operateur, Regle, BaseDeFaits

class BaseDeRegles: 

    def __init__(self):
        self.regles = []
    
    def __str__(self):
        chaine =  "======== Base de Rêgle ========\n"
        for regle in self.regles:
            chaine += str(regle) + "\n"
        chaine += "==============================="
        return chaine

    def ajouter(self, regle):
        if not isinstance(regle, Regle):
            raise TypeError("regle doit être une regle")
        self.regles.append(regle)

    def applicable(self, basedefaits):
        for regle in self.regles:
            if regle.applicable(basedefaits):
                return True
        return False      
    

    def regles_applicable(self, basedefaits):
        regles = []
        for regle in self.regles:
            if regle.applicable(basedefaits):
                regles.append(regle)
        return regles          
    
    def selection(self, basedefaits):
        for regle in self.regles:
            if regle.applicable(basedefaits):
                return regle
        return None

    def list_regles_ayant_conclusion(self, conclusion, basedefaits):
        ensemble_regle = []
        for regle in self.regles:
            if regle.contient_conclusion(conclusion, basedefaits):
                ensemble_regle.append(regle)
        return ensemble_regle

    def activer_tous(self):
        for regle in self.regles:
            regle.activer()
