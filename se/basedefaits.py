from se import Proposition, Operateur, Fait

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
                if fait == fait_a_verifier:
                    return True
        if isinstance(fait_a_verifier, Proposition):
            proposition_a_verifier = fait_a_verifier
            fait_a_verifier = proposition_a_verifier.en_fait(self)
            if isinstance(fait_a_verifier, bool):
                return fait_a_verifier
            for fait in self.faits:
                if proposition_a_verifier.operateur == Operateur.EGALITE:
                    if fait == fait_a_verifier:
                        return True
                elif proposition_a_verifier.operateur == Operateur.INEGALITE:
                    if fait != fait_a_verifier:
                        return True
                elif proposition_a_verifier.operateur == Operateur.INFERIORITE:
                    if fait < fait_a_verifier:
                        return True
                elif proposition_a_verifier.operateur == Operateur.INFERIORITEOUEGALITE:
                    if fait <= fait_a_verifier:
                        return True
                elif proposition_a_verifier.operateur == Operateur.SUPERIORITE:
                    if fait > fait_a_verifier:
                        return True
                elif proposition_a_verifier.operateur == Operateur.SUPERIORITEOUEGALITE:
                    if fait >= fait_a_verifier:
                        return True
        return False

    def ajouter(self, fait_a_ajouter):
        if isinstance(fait_a_ajouter, Fait):
            for fait in self.faits:
                if fait.symbole == fait_a_ajouter.symbole:
                    if fait.valeur == None:
                        fait.valeur = fait_a_ajouter.valeur
                        return
                    elif fait.valeur == fait_a_ajouter.valeur:
                        return
                    else:
                        raise Exception("ajout du fait imposible car le fait existe déjâ (inconsitante)")
            self.faits.append(fait_a_ajouter)

    def valeur_fait(self, symbole):
        for fait in self.faits:
            if fait.symbole == symbole:
                return fait.valeur
        self.ajouter(Fait(symbole, None))
        return None