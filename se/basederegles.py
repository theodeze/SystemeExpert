import collections
from se import Log, Fait, Proposition, Operateur, Regle, BaseDeFaits, SelectionRegle

class BaseDeRegles: 

    def __init__(self):
        self.regles = []
        self.strict = False
    
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

    def nom_regles(self, basedefaits):
        regles = "{ "
        for regles_applicale in self.regles_applicable(basedefaits):
            regles += regles_applicale.nom + " "
        regles += "}"
        return regles

    def peut_ajouter(self, regle_a_ajouter):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        conclusion_ok = True
        premisses_ok = True
        for regle in self.regles:
            if compare(regle_a_ajouter.conclusions, regle.conclusions):
                if self.strict:
                    Log.warning("Deux rêgles ont les même conclusion (Redondance)")
                else:
                    Log.debug("Deux rêgles ont les même conclusion (Redondance)")
                conclusion_ok = False
            if regle_a_ajouter.premisses == regle.premisses:
                if self.strict:
                    Log.warning("Deux rêgles ont les même premisse (Incompatibilité)")
                else:
                    Log.debug("Deux rêgles ont les même premisse (Incompatibilité)")
                premisses_ok = False  
        if self.strict:
            return conclusion_ok and premisses_ok
        return conclusion_ok or premisses_ok

    def ajouter(self, regle):
        Log.debug("Ajout de la rêgle " + str(regle))
        if self.peut_ajouter(regle):
            self.regles.append(regle)
        elif not self.strict:
            Log.warning("Ajout de la regle imposible car le regle existe déjâ (Inconsitante)")

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
        Log.debug("Selection d'une règle parmis " + self.nom_regles(basedefaits))
        Log.debug("Avec la règle " + selection_regle.value)
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
            for regle in self.regles:
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
