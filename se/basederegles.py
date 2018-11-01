from se import Fait, Proposition, Operateur, Regle, BaseDeFaits, SelectionRegle

class BaseDeRegles: 

    def __init__(self):
        self.regles = []
    
    def __str__(self):
        chaine =  "======== Base de Rêgle ========\n"
        for regle in self.regles:
            chaine += str(regle) + "\n"
        chaine += "==============================="
        return chaine

    def liste(self):
        liste = []
        for regle in self.regles:
            liste.append(str(regle))
        return liste

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
    
    @staticmethod
    def selection_tableau(tab_regle, basedefaits, selection_regle):
        if selection_regle == SelectionRegle.PREMIERE:
             return tab_regle[0]
        elif selection_regle == SelectionRegle.COMPLEXE:
            max_complexe = -1
            R = tab_regle[0]
            for regle in tab_regle:
                nb_complexe = len(regle.premisses)
                if nb_complexe > max_complexe:
                    R = regle
                    max_complexe = nb_complexe
            return R
        elif selection_regle == SelectionRegle.PLUS:
            max_plus = -1
            R = tab_regle[0]
            for regle in tab_regle:
                nb_plus = regle.nb_premisses_a_satisfaire(basedefaits)
                if nb_plus > max_plus:
                    R = regle
                    max_plus = nb_plus
            return R
        return None

    def selection(self, basedefaits, selection_regle):
        if selection_regle == SelectionRegle.PREMIERE:
            for regle in self.regles:
                if regle.applicable(basedefaits):
                    return regle
        elif selection_regle == SelectionRegle.COMPLEXE:
            max_complexe = -1
            R = None
            for regle in self.regles:
                if regle.applicable(basedefaits):
                    nb_complexe = len(regle.premisses)
                    if nb_complexe > max_complexe:
                        R = regle
                        max_complexe = nb_complexe
            return R
        elif selection_regle == SelectionRegle.PLUS:
            max_plus = -1
            R = None
            for regle in tab_regle:
                if regle.applicable(basedefaits):
                    nb_plus = regle.nb_premisses_a_satisfaire(basedefaits)
                    if nb_plus > max_plus:
                        R = regle
                        max_plus = nb_plus
            return R
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
