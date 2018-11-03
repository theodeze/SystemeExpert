import sys
from se import Log
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Stream(QObject):
    newText = Signal((str,))

    def __init__(self, afficher_commande):
        super(Stream, self).__init__()
        self.newText.connect(afficher_commande)

    def write(self, text):
        self.newText.emit(str(text))

class ColorationSyntax(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(ColorationSyntax, self).__init__(parent)
        self.regles = []

        motcles_format = QTextCharFormat()
        motcles_format.setForeground(Qt.blue)
        motcles_format.setFontWeight(QFont.Bold)
        # liste des mots à considérer
        motcles_motifs = ["TRACE", "LOG", "LIRE", "REGLE", "AIDE", "REINITIALISE",
                      "DEBUG", "INFO", "BF", "R[0-9]+"]
        motcles_motifs += ["TRUE", "FALSE", "VRAI", "FAUX"]
        for motcles_motif in motcles_motifs:
            motcles_regex = QRegExp("\\b" + motcles_motif + "\\b", 
                                                    Qt.CaseInsensitive)
            self.regles.append([motcles_regex, motcles_format])

        motimp_format = QTextCharFormat()
        motimp_format.setForeground(Qt.red)
        motimp_format.setFontWeight(QFont.Bold)
        motimp_motifs = ["WARNING", "ERROR", "CRITICAL"]
        for motimp_motif in motimp_motifs:
            motimp_regex = QRegExp("\\b" +  motimp_motif + "\\b", 
                                                    Qt.CaseInsensitive)
            self.regles.append([motimp_regex, motimp_format])

        operateur_format = QTextCharFormat()
        operateur_format.setForeground(Qt.blue)
        operateur_motif = "[⊢:∨∧<>!=&\|]+"
        operateur_regex = QRegExp(operateur_motif)
        self.regles.append([operateur_regex, operateur_format])


        delimiteur_format = QTextCharFormat()
        delimiteur_format.setForeground(Qt.red)
        delimiteur_motif = "[\)\(]+|[\{\}]+|[][]+"
        delimiteur_regex = QRegExp(delimiteur_motif)
        self.regles.append([delimiteur_regex, delimiteur_format])

        nombre_format = QTextCharFormat()
        nombre_format.setForeground(Qt.darkGreen)
        nombre_motif =  "\\b[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\\b"
        nombre_regex = QRegExp(nombre_motif)
        nombre_regex.setMinimal(True)
        self.regles.append([nombre_regex, nombre_format])

        chaine_format = QTextCharFormat()
        chaine_format.setForeground(Qt.red)
        chaine_motif = '\".*\"'
        chaine_regex = QRegExp(chaine_motif)
        chaine_regex.setMinimal(True)
        self.regles.append([chaine_regex, chaine_format])

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.gray)
        comment_motif = "#[^\n]*"
        comment_regex = QRegExp(comment_motif)
        self.regles.append([comment_regex, comment_format])

    def highlightBlock(self, text):
        for expression, tformat in self.regles:
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, tformat)
                index = expression.indexIn(text, index + length)


class Terminal(QWidget):
    mise_a_jour = Signal()

    def __init__(self, cli, parent = None):
        super(Terminal, self).__init__(parent)

        self.affichage = QTextBrowser(self)
        self.affichage.setFont(QFont("Overpass Mono", 10))
        self.coloration_syntax = ColorationSyntax(self.affichage.document())
        self.cli = cli

        self.commande = QLineEdit(self)
        self.commande.setFont(QFont("Overpass Mono", 10))
        self.commande.returnPressed.connect(self.envoyer_commande)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.affichage, 0, 0)
        self.layout.addWidget(self.commande, 1, 0)
        self.setLayout(self.layout)

        sys.stdout = Stream(self.afficher_commande)
        Log.init()
        
    def __del__(self):
        sys.stdout = sys.__stdout__
        Log.remove_log()

    def afficher_commande(self, text):
        cursor = self.affichage.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.affichage.setTextCursor(cursor)
        self.affichage.ensureCursorVisible()

    def envoyer_commande(self):
        print(">>> " + self.commande.text())
        self.cli.commande(self.commande.text())
        self.commande.clear()
        self.mise_a_jour.emit()
