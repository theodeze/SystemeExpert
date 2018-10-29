from se import Connecteur, Parenthese, Proposition, Operateur, Fait

class Regle:
    num = 1

    def __init__(self, premisses, conclusions):
        self.premisses = premisses
        self.conclusions = conclusions
        self.nom = "R" + str(Regle.num)
        Regle.num += 1
        self.est_desactive = False
    
    def __str__(self):        
        chaine = self.nom + " : "
        premiere = True
        index = 0
        for proposition in self.premisses:
            if premiere:
                if isinstance(proposition, Parenthese):
                    chaine += str(proposition.value)
                else:
                    chaine += str(proposition)
                premiere = False
            else:
                if isinstance(proposition, Connecteur) or isinstance(proposition, Parenthese):
                    chaine += " " + str(proposition.value)
                else:
                    chaine += " " + str(proposition)
                index += 1
        premiere = True
        chaine += " ⊢ "
        for proposition in self.conclusions:
            if premiere:
                chaine += str(proposition)
                premiere = False
            else:
                chaine += " ∧ " + str(proposition)
        return chaine

    @staticmethod
    def conversion_infixee_en_postfixee(lexemes):
        lexemes_sortie = []
        pile_operateurs = []
        for lex in lexemes:
            if isinstance(lex, Proposition):
                lexemes_sortie.append(lex)
            elif isinstance(lex, Connecteur):
                    pile_operateurs.append(lex)
            elif isinstance(lex, Parenthese):
                if lex == Parenthese.OUVRANT:
                    pile_operateurs.append(lex)
                elif lex == Parenthese.FERMANT:
                    while pile_operateurs[-1] != Parenthese.OUVRANT :
                        lexemes_sortie.append(pile_operateurs.pop())
                    pile_operateurs.pop()
        while len(pile_operateurs) != 0:
            lexemes_sortie.append(pile_operateurs.pop())
        return lexemes_sortie

    def applicable(self, basedefaits):
        if self.est_desactive:
            return False
        pile_valeurs = []
        for lex in Regle.conversion_infixee_en_postfixee(self.premisses):
            if isinstance(lex, Proposition):
                pile_valeurs.append(lex.valeur(basedefaits))
            elif isinstance(lex, Connecteur):
                if len(pile_valeurs) < 2:
                    raise Exception("Erreur dans l'expression")
                if lex == Connecteur.ET:
                    valeur_droite = pile_valeurs.pop()
                    valeur_gauche = pile_valeurs.pop()
                    pile_valeurs.append(valeur_gauche and valeur_droite)
                elif lex == Connecteur.OU:
                    valeur_droite = pile_valeurs.pop()
                    valeur_gauche = pile_valeurs.pop()
                    pile_valeurs.append(valeur_gauche or valeur_droite)
        if len(pile_valeurs) != 1:
            raise Exception("Erreur dans l'expression")
        return pile_valeurs[0]

    def contient_conclusion(self, conclusion_a_chercher, basedefaits):
        if isinstance(conclusion_a_chercher, Fait):
            for conclusion in self.conclusions:
                if conclusion == conclusion_a_chercher:
                    return True   
        if isinstance(conclusion_a_chercher, Proposition):
            fait = conclusion_a_chercher.en_fait(basedefaits)
            if isinstance(fait, bool):
                return False
            for conclusion in self.conclusions:
                if conclusion_a_chercher.operateur == Operateur.EGALITE:
                    if fait == conclusion:
                        return True
                elif conclusion_a_chercher.operateur == Operateur.INEGALITE:
                    if fait != conclusion:
                        return True
                elif conclusion_a_chercher.operateur == Operateur.SUPERIORITE:
                    if fait > conclusion:
                        return True
                elif conclusion_a_chercher.operateur == Operateur.SUPERIORITEOUEGALITE:
                    if fait >= conclusion:
                        return True
                elif conclusion_a_chercher.operateur == Operateur.INFERIORITE:
                    if fait < conclusion:
                        return True
                elif conclusion_a_chercher.operateur == Operateur.INFERIORITEOUEGALITE:
                    if fait <= conclusion:
                        return True
        return False

    def appliquer(self, basedefaits):
        if not self.est_desactive:
            for fait in self.conclusions:
                basedefaits.ajouter(fait)