from base import Fait, Proposition, Operateur
from basedefaits import BaseDeFaits 
from basederegles import BaseDeRegles
from pptree import *

class MoteurDInferance:

    def __init__(self, debug):
        self.debug = debug

    def chainage_avant(self, basedefaits, basederegle, fait_a_etablir):
        if not isinstance(basedefaits, BaseDeFaits):
            raise TypeError("basedefaits doit être une BaseDeFaits")
        if not isinstance(basederegle, BaseDeRegles):
            raise TypeError("basederegle doit être une BaseDeRegles")
        if not isinstance(fait_a_etablir, Fait):
            raise TypeError("fait_a_etablir doit être un Fait")
        iteration = 1
        while not basedefaits.contient(fait_a_etablir) and basederegle.applicable(basedefaits):
            regle = basederegle.selection(basedefaits)
            if self.debug:
                print("Iteration " + str(iteration) + " :")
                print(regle)
                iteration += 1
            regle.appliquer(basedefaits)
            regle.desactiver()
        print("============= Résultat chainage avant")
        print(str(fait_a_etablir))
        if basedefaits.contient(fait_a_etablir):
            print("Fait établie")
        else:
            print("Fait non établie")
        print("=============")
        return basedefaits.contient(fait_a_etablir)

    def chainage_arriere(self, basedefaits, basederegles, fait_a_etablir, noeud_parent):
        if basedefaits.contient(fait_a_etablir):
            Node(str(fait_a_etablir) + " dans BF", noeud_parent)
            return True
        if noeud_parent == None:
            noeud = Node(str(fait_a_etablir))
        else:
            noeud = Node(str(fait_a_etablir), noeud_parent)
        ER = basederegles.list_regles_ayant_conclusion(fait_a_etablir)
        R = None
        valide = False
        while valide != True and ER != []:
            valide = True
            R = ER[0]
            noeud2 = Node(str(R), noeud)
            ER.pop(0)
            for Fr in R.liste_premisses():
                valide = valide and self.chainage_arriere(basedefaits, basederegles, Fr, noeud2)
        if valide:
            basedefaits.ajouter_fait(fait_a_etablir)
            for conclusion in R.liste_conclusions():
                basedefaits.ajouter_fait(conclusion)
        elif noeud_parent != None:
            Node(" echec", noeud)
        if noeud_parent == None:
            print("============= Résultat chainage arriere")
            print_tree(noeud)
        return valide

#DEBUT
#SI (F∈ BF) ALORS ChaînageArriere  OK
#    SINON construire ER ensemble de règles R, telle que F ∈ conclusion(R)
#    FAIRE 
#        valide  VRAI
#        R  premier element de ER
#        ER  ER – {R}
#        POURTOUT Fr ∈ premisse(R)
#            valide  valide ET ChaînageArriere (BF, BR, Fr)
#        FIN POUR 
#    JUSQU’À (valide OU ER ≠∅ )
#SI valide ALORS BF = BF ∪ {F}
#ChaînageArriere  valide
#FIN