from basedefaits import BaseDeFaits, Fait
from basederegles import BaseDeRegle

class MoteurDInferance:

    def chainage_avant(self, basedefaits, basederegle, fait_a_etablir):
        if not isinstance(basedefaits, BaseDeFaits):
            raise TypeError("basedefaits doit être une BaseDeFaits")
        if not isinstance(basederegle, BaseDeRegle):
            raise TypeError("basederegle doit être une BaseDeRegle")
        if not isinstance(fait_a_etablir, Fait):
            raise TypeError("fait_a_etablir doit être un Fait")
        while not basedefaits.contiant(fait_a_etablir) and basederegle.applicable(basedefaits):
            regle = basederegle.selection(basedefaits)
            regle.appliquer(basedefaits)
            regle.desactiver()
        return basedefaits.contiant(fait_a_etablir)
        