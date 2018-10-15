# coding=utf8

from basedefaits import BaseDeFaits, Fait
from basederegles import BaseDeRegles

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
        
    def chainage_arriere(self, basedefaits, basederegle, fait_a_etablir):
        print("============= Résultat chainage arriere")
