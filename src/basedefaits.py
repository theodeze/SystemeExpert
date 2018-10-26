from .base import Proposition, Operateur, Fait

class BaseDeFaits:
    
    def __init__(self):
        self.faits = []

    def __str__(self):
        chaine =  "======== Base de Faits ========\n"
        for fait in self.faits:
            chaine += str(fait) + "\n"
        chaine += "==============================="
        return chaine

    def to_array(self):
        array = []
        for fait in self.faits:
            array.append(str(fait))
        return array

    def contient(self, fait_a_verifier):
        if isinstance(fait_a_verifier, Fait):
            for fait in self.faits:
                if Fait.egale(fait, fait_a_verifier):
                    return True
        if isinstance(fait_a_verifier, Proposition):
            proposition_a_verifier = fait_a_verifier
            fait_a_verifier = proposition_a_verifier.en_fait(self)
            if isinstance(fait_a_verifier, bool):
                return fait_a_verifier
            elif fait_a_verifier != None:
                for fait in self.faits:
                    if proposition_a_verifier.operateur == Operateur.EGALITE:
                        if Fait.egale(fait_a_verifier, fait):
                            return True
                    elif proposition_a_verifier.operateur == Operateur.INEGALITE:
                        if Fait.inegale(fait_a_verifier, fait):
                            return True
                    elif proposition_a_verifier.operateur == Operateur.INFERIORITE:
                        if Fait.inferieur(fait_a_verifier, fait):
                            return True
                    elif proposition_a_verifier.operateur == Operateur.INFERIORITEOUEGALITE:
                        if Fait.inferieur_egale(fait_a_verifier, fait):
                            return True
                    elif proposition_a_verifier.operateur == Operateur.SUPERIORITE:
                        if Fait.superieur(fait_a_verifier, fait):
                            return True
                    elif proposition_a_verifier.operateur == Operateur.SUPERIORITEOUEGALITE:
                        if Fait.superieur_egale(fait_a_verifier, fait):
                            return True
        return False

    def ajouter_fait(self, fait_a_ajouter):
        if isinstance(fait_a_ajouter, Fait):
            for fait in self.faits:
                if fait.nom == fait_a_ajouter.nom:
                    if fait.valeur == None:
                        fait.valeur = fait_a_ajouter.valeur
                        return
                    elif fait.valeur == fait_a_ajouter.valeur:
                        return
                    else:
                        raise Exception("ajout du fait imposible car le fait existe déjâ (inconsitante)")
            self.faits.append(fait_a_ajouter)

    def valeur_fait(self, nom):
        for fait in self.faits:
            if fait.nom == nom:
                return fait.valeur
        self.ajouter_fait(Fait(nom, None))
        return None