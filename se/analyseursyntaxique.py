import re
from se import Log, Operateur, Parenthese, Connecteur, Fait, Proposition, Regle, AnalyseurSimple

class AnalyseurSyntaxique(AnalyseurSimple):

    @staticmethod
    def analyse_symbole(symbole):
        symbole = symbole.strip()
        if symbole.isdigit():
            raise Exception("N'est pas un symbole valide {}".format(symbole))
        elif symbole == "True" or symbole == "Vrai":
            raise Exception("N'est pas un symbole valide {}".format(symbole))
        elif symbole == "False" or symbole == "Faux":
            raise Exception("N'est pas un symbole valide {}".format(symbole))
        elif symbole.startswith('"') and symbole.endswith('"'):
            raise Exception("N'est pas un symbole valide {}".format(symbole))
        else:
            return symbole

    @staticmethod
    def analyse_valeur(valeur):
        valeur = valeur.strip()
        if valeur.isdigit():
            return float(valeur)
        elif valeur == "True" or valeur == "Vrai":
            return True
        elif valeur == "False" or valeur == "Faux":
            return False
        else:
            return valeur

    @staticmethod
    def analyse_valeur_fait(valeur):
        valeur = valeur.strip()
        if valeur.isdigit():
            return float(valeur)
        elif valeur == "True" or valeur == "Vrai":
            return True
        elif valeur == "False" or valeur == "Faux":
            return False
        elif valeur.startswith("\"") and valeur.endswith("\""):
            return valeur
        else:
            raise Exception("N'est pas une valeur valide {}".format(valeur))

    @staticmethod
    def verifier_valeurs(valeurs, lexeme):
        if len(valeurs) == 0:
            raise Exception("il manque deux valeurs {}".format(lexeme))
        if len(valeurs) == 1:
            raise Exception("il manque un valeur {}".format(lexeme))
        if valeurs[0].strip() == "" or valeurs[1].strip() == "":
            raise Exception("Une valeur ne peut être vide {}".format(lexeme))
        
    @staticmethod
    def analyse_premise(chaine):
        lexemes = []
        nb_parenthese = 0
        for lexeme in re.split(r'(&+|\|\|+|\(+|\)+)', chaine):
            if Parenthese.OUVRANT.value in lexeme:
                nb_parenthese += 1
                lexemes.append(Parenthese.OUVRANT)
            elif Parenthese.FERMANT.value in lexeme:
                nb_parenthese -= 1
                lexemes.append(Parenthese.FERMANT)
            elif '&' in lexeme:
                lexemes.append(Connecteur.ET)
            elif '||' in lexeme:
                lexemes.append(Connecteur.OU)
            elif Operateur.EGALITE.value in lexeme:
                valeurs = lexeme.split(Operateur.EGALITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.EGALITE, valeur_droite))
            elif Operateur.INEGALITE.value in lexeme:
                valeurs = lexeme.split(Operateur.INEGALITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.INEGALITE, valeur_droite))
            elif Operateur.SUPERIORITE.value in lexeme:
                valeurs = lexeme.split(Operateur.SUPERIORITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.SUPERIORITE, valeur_droite))
            elif Operateur.SUPERIORITEOUEGALITE.value in lexeme:
                valeurs = lexeme.split(Operateur.SUPERIORITEOUEGALITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.SUPERIORITEOUEGALITE, valeur_droite))
            elif Operateur.INFERIORITE.value in lexeme:
                valeurs = lexeme.split(Operateur.INFERIORITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.INFERIORITE, valeur_droite))
            elif Operateur.INFERIORITEOUEGALITE.value in lexeme:
                valeurs = lexeme.split(Operateur.INFERIORITEOUEGALITE.value)
                AnalyseurSyntaxique.verifier_valeurs(valeurs, lexeme)
                valeur_gauche = AnalyseurSyntaxique.analyse_valeur(valeurs[0])
                valeur_droite = AnalyseurSyntaxique.analyse_valeur(valeurs[1])
                lexemes.append(Proposition(valeur_gauche, Operateur.INFERIORITEOUEGALITE, valeur_droite))
            elif lexeme.strip() != "":
                raise Exception("Non valide {}".format(lexeme))
        if nb_parenthese != 0:
             raise Exception("Il manque une parenthèse")
        return lexemes

    @staticmethod
    def analyse_conclusion(chaine):
        conclusions = []
        for conclusion in chaine.split("&"):
            if len(conclusion.split("=")) < 2:
                raise Exception("Invalide {}".format(chaine))
            symbole = AnalyseurSyntaxique.analyse_symbole(conclusion.split("=")[0])
            valeur = AnalyseurSyntaxique.analyse_valeur_fait(conclusion.split("=")[1])
            conclusions.append(Fait(symbole, valeur))
        return conclusions

    @staticmethod
    def analyse_regle(chaine):
        if len(chaine.split(":=")) < 2:
            raise Exception("Invalide {}".format(chaine)) 
        conclusions = AnalyseurSyntaxique.analyse_conclusion(chaine.split(":=")[0])
        premisses = AnalyseurSyntaxique.analyse_premise(chaine.split(":=")[1])
        return Regle(premisses, conclusions)

    @staticmethod
    def analyse_fait(chaine):
        if len(chaine.split("=")) < 2:
            raise Exception("Invalide {}".format(chaine))
        AnalyseurSyntaxique.verifier_valeurs(chaine.split("="), chaine)
        symbole = AnalyseurSyntaxique.analyse_symbole(chaine.split("=")[0])
        valeur = AnalyseurSyntaxique.analyse_valeur_fait(chaine.split("=")[1])
        return Fait(symbole, valeur)

    @staticmethod
    def retire_commentaire(chaine):
        return chaine.split("#")[0]

    @staticmethod
    def analyse_ligne(chaine, basedefaits, basederegles):
        if ":=" in chaine:
            try:
                basederegles.ajouter(AnalyseurSyntaxique.analyse_regle(chaine))
            except Exception as e:
                Log.warning("{}".format(e))          
        elif "=" in chaine:
            try:
                basedefaits.ajouter(AnalyseurSyntaxique.analyse_fait(chaine))
            except Exception as e:
                Log.warning("{}".format(e))    
        elif chaine.strip() != "":
            Log.warning("Non reconnus {}".format(chaine))       

    @staticmethod
    def analyse_fichier(nom_fichier, basedefaits, basederegles):
        with open(nom_fichier) as fichier:
            for ligne in fichier:
                chaine = AnalyseurSyntaxique.retire_commentaire(ligne.split("\n")[0])
                AnalyseurSyntaxique.analyse_ligne(chaine, basedefaits, basederegles)
        fichier.close()
     