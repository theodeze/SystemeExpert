
from basedefaits import *
from basederegles import *
from lecteur import *
# from moteurdinference import *

#    une base de faits
#    une base de règles
#    un moteur d'inférence.


basedefaits = BaseDeFaits()
basederegles = BaseDeRegles()
lecteur = Lecteur()
lecteur.lire_fichier(basedefaits,basederegles)
#basedefaits.ajouter_fait(Fait("Taille de Thomas", 175))
#basedefaits.ajouter_fait(Fait("Taille de Gidéone", 169))
#basedefaits.ajouter_fait(Fait("Grand", True))
print(basedefaits)

regle1 = Regle(Proposition("Grand", Operateur.AFFECTATION, True))
regle1.ajouter_premisse(Proposition("Taille de Thomas", Operateur.SUPERIORITE, 150))

basederegles.ajouter_regle(regle1)
print(basederegles)

regle = basederegles.selection(basedefaits)
regle.appliquer(basedefaits)
print(basedefaits)


