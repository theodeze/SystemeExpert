class Fait:

    def __init__(self, symbole, valeur):
        self.symbole = symbole
        self.valeur = valeur

    def __str__(self):
        if isinstance(self.valeur, bool) and self.valeur:
            return "{}".format(self.symbole)
        if isinstance(self.valeur, bool) and not self.valeur:
            return "¬{}".format(self.symbole)
        return "{} ≔ {}".format(self.symbole, self.valeur)

    def __hash__(self):
        return hash(self.symbole) + hash(self.valeur)

    def __eq__(self, fait):
        if not isinstance(fait, Fait):
            return False
        return self.symbole == fait.symbole and self.valeur == fait.valeur

    def __ne__(self, fait):
        return self.symbole == fait.symbole and self.valeur != fait.valeur

    def __gt__(self, fait):
        return self.symbole == fait.symbole and self.valeur > fait.valeur

    def __ge__(self, fait):
        return self.symbole == fait.symbole and self.valeur >= fait.valeur

    def __lt__(self, fait):
        return self.symbole == fait.symbole and self.valeur < fait.valeur

    def __le__(self, fait):
        return self.symbole == fait.symbole and self.valeur <= fait.valeur

    def pair(self):
        return (self.symbole, self.valeur)