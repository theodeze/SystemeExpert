from .base import Fait, Proposition, Operateur
from .basedefaits import BaseDeFaits 
from .basederegles import BaseDeRegles
from pptree import *

class MoteurDInferance:

    def __init__(self, debug):
        self.debug = debug

    def chainage_avant(self, basedefaits, basederegle, fait_a_etablir):
        iteration = 1
        valide = basedefaits.contient(fait_a_etablir)
        while not valide and basederegle.applicable(basedefaits):
            regle = basederegle.selection(basedefaits)
            if self.debug:
                print("Iteration " + str(iteration) + " :")
                print(regle)
                iteration += 1
            regle.appliquer(basedefaits)
            regle.desactiver()
            valide = basedefaits.contient(fait_a_etablir)
        
        # Affichage résultat
        print("=== Résultat chainage avant ===")
        print(str(fait_a_etablir))
        if valide:
            print("Fait établie")
        else:
            print("Fait non établie")
        print("===============================")

        return valide

    def chainage_arriere(self, basedefaits, basederegles, fait_a_etablir, noeud_parent, faits_precedent):
        if basedefaits.contient(fait_a_etablir):
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

        ER = basederegles.list_regles_ayant_conclusion(fait_a_etablir)
        R = None
        valide = False
        while not valide and ER != []:
            valide = True # plus besoin
            R = ER[0]
            noeud2 = Node(str(R), noeud)
            ER.pop(0)
            index = -1
            for Fr in R.liste_premisses():
                if index == -1:
                    valide = self.chainage_arriere(basedefaits, basederegles, Fr, noeud2, faits_precedent)
                    index += 1
                elif R.operateurs[index] == Operateur.ET:
                    valide = valide and self.chainage_arriere(basedefaits, basederegles, Fr, noeud2, faits_precedent)
                    index +=1
                elif R.operateurs[index] == Operateur.OU:
                    valide = valide or self.chainage_arriere(basedefaits, basederegles, Fr, noeud2, faits_precedent)
                    index +=1
        if valide:
            basedefaits.ajouter_fait(fait_a_etablir)
            for conclusion in R.liste_conclusions():
                basedefaits.ajouter_fait(conclusion)
        elif noeud_parent != None:
            Node("Echec", noeud)
            return False

        # Affichage résultat
        if noeud_parent == None:
            print("== Résultat chainage arriere ==")
            print_tree(noeud)
            print("===============================")
            print(str(fait_a_etablir))
            if valide:
                print("Fait établie")
            else:
                print("Fait non établie")
            print("===============================")

        return valide
