
import sys
from se import CLI, AnalyseurSyntaxique, Fait
from PySide2.QtCore import QObject, QStringListModel, Signal, Slot, Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QTextCursor

class Stream(QObject):
    newText = Signal((str,))

    def __init__(self, afficher_commande):
        super(Stream, self).__init__()
        self.newText.connect(afficher_commande)

    def write(self, text):
        self.newText.emit(str(text))


class Dock(QDockWidget):

    def __init__(self, cli, parent = None):
        super(Dock, self).__init__(parent)
        self.cli = cli
        
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.affichage_basedefaits = QTableWidget(1, 2)
        self.basederegles = QListView()
        self.basederegles.mouseMoveEvent = self.clique_basederegles

        self.affichage_basedefaits.setHorizontalHeaderLabels(["Symbole","Valeur"])
        self.affichage_basedefaits.cellChanged.connect(self.modification_basedefaits)
        self.affichage_basedefaits.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        model = QStringListModel(self)
        self.basederegles.setModel(model)

        self.mise_a_jour_basedefaits([("a", True), ("b", 25.2), ("c", False)])

        model.setStringList(["ss","ssss"])

        self.widget = QWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        self.layout.addWidget(QLabel("Base de Faits"), 0, 0)
        self.layout.addWidget(self.affichage_basedefaits, 1, 0)
        self.layout.addWidget(QLabel("Base de Règles"), 2, 0)
        self.layout.addWidget(self.basederegles, 3, 0)
        self.setWidget(self.widget)

    def clique_basederegles(self):
        print("Salut")

    def mise_a_jour_basedefaits(self, donnees):
        ligne = 0
        for symbole, valeur in donnees:
            self.affichage_basedefaits.setItem(ligne, 0, QTableWidgetItem(symbole))
            self.affichage_basedefaits.setItem(ligne, 1, QTableWidgetItem(str(valeur)))
            ligne += 1

    def modification_basedefaits(self, ligne):
        if self.affichage_basedefaits.item(ligne, 0) is None or self.affichage_basedefaits.item(ligne, 1) is None:
            return
        symbole = self.affichage_basedefaits.item(ligne, 0).text().strip()
        valeur = self.affichage_basedefaits.item(ligne, 1).text().strip()
        if symbole != "" and valeur != "":
            try:
                AnalyseurSyntaxique.analyse_symbole(symbole)
                if self.affichage_basedefaits.rowCount() - 1 != ligne:
                    self.cli.basedefaits.modifier(ligne, Fait(symbole, AnalyseurSyntaxique.analyse_valeur(valeur)))
                else:
                    self.cli.basedefaits.ajouter(Fait(symbole, AnalyseurSyntaxique.analyse_valeur(valeur)))
                    self.affichage_basedefaits.setRowCount(self.affichage_basedefaits.rowCount() + 1)
            except Exception:
                self.affichage_basedefaits.setItem(ligne, 0, QTableWidgetItem(""))


class Terminal(QWidget):

    def __init__(self, cli, parent = None):
        super(Terminal, self).__init__(parent)

        self.affichage = QTextBrowser(self)
        self.cli = cli

        self.commande = QLineEdit(self)
        self.commande.returnPressed.connect(self.envoyer_commande)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.affichage, 0, 0)
        self.layout.addWidget(self.commande, 1, 0)
        self.setLayout(self.layout)

        sys.stdout = Stream(self.afficher_commande)
        
    def __del__(self):
        sys.stdout = sys.__stdout__
    
    def afficher_commande(self, text):
        cursor = self.affichage.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.affichage.setTextCursor(cursor)
        self.affichage.ensureCursorVisible()

    def envoyer_commande(self):
        self.cli.commande(self.commande.text())
        self.commande.clear()


class FenetrePrincipal(QMainWindow):

    def __init__(self, parent = None):
        super(FenetrePrincipal, self).__init__(parent)
        cli = CLI()
        self.setWindowTitle("Systeme Expert")
        self.setMinimumSize(1280, 720)
        self.terminal = Terminal(cli, self)
        self.setCentralWidget(self.terminal)
        self.dock = Dock(cli, self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock);


def main_gui():
    app = QApplication(sys.argv)
    mainwindow = FenetrePrincipal()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main_gui()