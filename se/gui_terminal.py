import sys
from se import Log, ColorationSyntax
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


class LigneCommande(QTextEdit):
    returnPressed = Signal()

    def __init__(self, ):
        super(LigneCommande, self).__init__()
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(28)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return  or event.key() == Qt.Key_Enter:
            self.returnPressed.emit() 
        else:
            super(LigneCommande, self).keyPressEvent(event)

class Terminal(QWidget):
    mise_a_jour = Signal()

    def __init__(self, cli, parent = None):
        super(Terminal, self).__init__(parent)

        self.affichage = QTextBrowser()
        self.affichage.setFont(QFont("Overpass Mono", 10))
        self.affichage.setStyleSheet("color: #2A2B32; background: #F8F8F8;")
        self.coloration_syntax = ColorationSyntax(self.affichage.document())
        self.cli = cli

        self.commande = LigneCommande()
        self.commande.setFont(QFont("Overpass Mono", 10))
        self.commande.setStyleSheet("color: #2A2B32; background: #F8F8F8;")
        self.commande.returnPressed.connect(self.envoyer_commande)
        ColorationSyntax(self.commande.document())

        self.layout = QGridLayout()
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
        print(">>> " + self.commande.toPlainText())
        self.cli.commande(self.commande.toPlainText())
        self.commande.clear()
        self.mise_a_jour.emit()
