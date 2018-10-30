from se import Fait, Proposition, Operateur, BaseDeFaits, BaseDeRegles, Connecteur, Regle, Trace, SelectionRegle
from pptree import *

class MoteurDInferance:

    def __init__(self):
        self.trace = Trace.NON
        self.selection_regle = SelectionRegle.PREMIERE

    def chainage_avant(self, basedefaits, basederegles, fait_a_etablir):
        iteration = 1
        valide = basedefaits.contient(fait_a_etablir)
        while not valide and basederegles.applicable(basedefaits):
            regle = basederegles.selection(basedefaits, self.selection_regle)
            if self.trace == Trace.MIN:
                print("===============================")
                print("Iteration " + str(iteration) + " :")
                print("Déclenchement de " + regle.nom)
            elif self.trace == Trace.OUI:
                print("===============================")
                print("Iteration " + str(iteration))
                regles = "{ "
                for regles_applicale in basederegles.regles_applicable(basedefaits):
                    regles += regles_applicale.nom + " "
                regles += "}"
                print("Règles déclenchables : " + regles)
                print("Déclenchement de " + regle.nom)
            regle.appliquer(basedefaits)
            if self.trace == Trace.OUI:
                faits = "{ "
                for fait in regle.conclusions:
                    faits += str(fait) + " "
                faits += "}"
                print("Ajout des faits : " + faits)
            regle.est_desactive = True
            valide = basedefaits.contient(fait_a_etablir)
            iteration += 1
        
        # Affichage résultat
        print("=== Résultat chainage avant ===")
        print(str(fait_a_etablir))
        if valide:
            print("Fait établie")
        else:
            print("Fait non établie")
        print("===============================")

        for regle in basederegles.regles:
            regle.est_desactive = False

        return valide

    def chainage_arriere(self, basedefaits, basederegles, fait_a_etablir, noeud_parent, faits_precedent):
        if basedefaits.contient(fait_a_etablir):
            if noeud_parent == None:
                print("== Résultat chainage arriere ==")
                print(str(fait_a_etablir))
                print("Fait établie")
                print("===============================")
            Node(str(fait_a_etablir) + " dans BF", noeud_parent)
            return True
        
        # Gestion de l'arbre
        if noeud_parent == None:
            noeud = Node(str(fait_a_etablir))
            faits_precedent = []
        else:
            noeud = Node(str(fait_a_etablir), noeud_parent)

        # Gestion des Blogages circulaire
        if faits_precedent == None:
            faits_precedent = []
        elif fait_a_etablir in faits_precedent:
            Node("Bouclage", noeud)
            return False
        faits_precedent.append(fait_a_etablir)

        ER = basederegles.list_regles_ayant_conclusion(fait_a_etablir, basedefaits)
        R = None
        valide = False
        while not valide and ER != []:
            valide = True # plus besoin
            R = ER[0]
            noeud2 = Node(str(R), noeud)
            ER.pop(0)
            pile_valeurs = []
            for lex in Regle.conversion_infixee_en_postfixee(R.premisses):
                if isinstance(lex, Proposition):
                    pile_valeurs.append(self.chainage_arriere(basedefaits, basederegles, lex, noeud2, faits_precedent))
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
            valide = pile_valeurs[0]
        if valide:
            basedefaits.ajouter(fait_a_etablir)
            for conclusion in R.conclusions:
                basedefaits.ajouter(conclusion)
        elif noeud_parent != None:
            Node("Echec", noeud)
            return False

        # Affichage résultat
        if noeud_parent == None:
            if self.trace != Trace.NON:
                print("===============================")
                print_tree(noeud)
            print("== Résultat chainage arriere ==")
            print(str(fait_a_etablir))
            if valide:
                print("Fait établie")
            else:
                print("Fait non établie")
            print("===============================")

        return valide
