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

    def modifier(self, ligne, fait_a_modifier):
        if isinstance(fait_a_modifier, Fait):
            if not self.peut_modifier(ligne, fait_a_modifier.symbole):
                raise Exception("Le symbole est déja pris")
            index = 0
            for fait in self.faits:
                if index == ligne:
                    fait.symbole = fait_a_modifier.symbole
                    fait.valeur = fait_a_modifier.valeur
                    return
                index += 1

    def symbole(self, ligne):
        index = 0
        for fait in self.faits:
            if index == ligne:
                return fait.symbole
            index += 1
        return ""

    def peut_modifier(self, ligne, symbole):
        index = 0
        for fait in self.faits:
            if fait.symbole == symbole:
                if ligne != index:
                    return False
            index += 1
        return True

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

    def pairs(self):
        pairs = []
        for fait in self.faits:
            pairs.append(fait.pair())
        return pairs