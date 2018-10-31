
import sys
from se import CLI, AnalyseurSyntaxique, Fait, Trace, SelectionRegle, Aide, DemandeFait, Configuration, APropos
from PySide2.QtCore import QObject, QStringListModel, Signal, Slot, Qt, QTranslator, QLocale, QLibraryInfo
from PySide2.QtWidgets import *
from PySide2.QtGui import QTextCursor, QIcon

class Stream(QObject):
    newText = Signal((str,))

    def __init__(self, afficher_commande):
        super(Stream, self).__init__()
        self.newText.connect(afficher_commande)

    def write(self, text):
        self.newText.emit(str(text))


class AffichageBaseDeConnaissance(QWidget):

    def __init__(self, cli, parent = None):
        super(AffichageBaseDeConnaissance, self).__init__(parent)
        self.cli = cli
        self.affichage_basedefaits = QTableWidget(1, 2)
        self.affichage_basedefaits.setHorizontalHeaderLabels(["Symbole","Valeur"])
        self.affichage_basedefaits.cellChanged.connect(self.modification_basedefaits)
        self.affichage_basedefaits.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.affichage_basederegles = QListWidget()
        self.affichage_basederegles.setWrapping(True)
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Base de Faits"), 0, 0)
        self.layout.addWidget(self.affichage_basedefaits, 1, 0)
        self.layout.addWidget(QLabel("Base de Règles"), 2, 0)
        self.layout.addWidget(self.affichage_basederegles, 3, 0)
        self.desactiver_modification = False
        self.setLayout(self.layout)

    def mise_a_jour_basedefaits(self):
        self.desactiver_modification = True
        ligne = 0
        for symbole, valeur in self.cli.basedefaits.pairs():
            self.affichage_basedefaits.setItem(ligne, 0, QTableWidgetItem(symbole))
            self.affichage_basedefaits.setItem(ligne, 1, QTableWidgetItem(str(valeur)))
            ligne += 1
        self.desactiver_modification = False

    def mise_a_jour_basederegles(self):
        self.affichage_basederegles.clear()
        self.affichage_basederegles.addItems(self.cli.basederegles.liste())

    def modification_basedefaits(self, ligne):
        if self.affichage_basedefaits.item(ligne, 0) is None or self.affichage_basedefaits.item(ligne, 1) is None:
            return
        if self.desactiver_modification:
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
                self.affichage_basedefaits.setItem(ligne, 0, QTableWidgetItem(self.cli.basedefaits.symbole(ligne)))


class Dock(QDockWidget):

    def __init__(self, cli, parent = None):
        super(Dock, self).__init__(parent)
        self.setWindowTitle("Base de connaissance")
        self.cli = cli
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.affichage_base_de_connaissance = AffichageBaseDeConnaissance(cli)
        self.setWidget(self.affichage_base_de_connaissance)


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


class BarreCommande(QToolBar):
    mise_a_jour = Signal() 

    def __init__(self, cli, parent = None):
        super(BarreCommande, self).__init__(parent)
        self.cli = cli
        self.setWindowTitle("Barre de commande")
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon	)
        self.addAction(QIcon("res/baseline-library_add-24px.svg"), "Charger fichier", self.Charge_fichier)
        self.addSeparator()
        self.addAction(QIcon("res/baseline-arrow_back-24px.svg"), "Chaînage avant", self.chainage_avant)
        self.addAction(QIcon("res/baseline-arrow_forward-24px.svg"), "Chaînage arriere", self.chainage_arriere)
        self.addSeparator()
        self.addAction(QIcon("res/baseline-settings-20px.svg"), "Configuration", self.configuration)
        self.addAction(QIcon("res/baseline-help-24px.svg"), "Aide", self.aide)

    def Charge_fichier(self):
        nom_fichier = QFileDialog.getOpenFileName(self, "Charger fichier")[0]
        if nom_fichier != "":
            self.cli.lire_fichier(nom_fichier)
            self.mise_a_jour.emit()

    def chainage_avant(self):
        demandefait = DemandeFait("Chaînage avant", self)
        rep = demandefait.exec()
        if rep == QDialog.Accepted:
            self.cli.moteur.chainage_avant(self.cli.basedefaits, self.cli.basederegles, 
            Fait(demandefait.symbole.text(), AnalyseurSyntaxique.analyse_valeur(demandefait.valeur.text())))
            self.mise_a_jour.emit()

    def chainage_arriere(self):
        demandefait = DemandeFait("Chaînage arrière", self)
        rep = demandefait.exec()
        if rep == QDialog.Accepted:
            self.cli.moteur.chainage_arriere(self.cli.basedefaits, self.cli.basederegles, 
            Fait(demandefait.symbole.text(), AnalyseurSyntaxique.analyse_valeur(demandefait.valeur.text())), None, None)
            self.mise_a_jour.emit()

    def configuration(self):
        configuration = Configuration(self.cli, self)
        rep = configuration.exec()
        if rep == QDialog.Accepted:
            print("A")

    def aide(self):
        aide = Aide(self)
        aide.exec()


class Menu(QMenuBar):

    def __init__(self, parent = None):
        super(Menu, self).__init__(parent)
        self.fichier = self.addMenu("Fichier")
        self.fichier.addAction("Ouvrire fichier")
        self.fichier.addSeparator()
        self.fichier.addAction("Quitter", QApplication.quit)
        self.affichage = self.addMenu("Affichage")
        self.aide = self.addMenu("Aide")
        self.aide.addAction("Contenu...", self.contenu)
        self.aide.addSeparator()
        self.aide.addAction("A propos", self.apropos)

    def contenu(self):
        aide = Aide(self)
        aide.exec()

    def apropos(self):
        apropos = APropos(self)
        apropos.exec()


class FenetrePrincipal(QMainWindow):

    def __init__(self, parent = None):
        super(FenetrePrincipal, self).__init__(parent)
        cli = CLI()
        self.setWindowTitle("Système Expert")
        self.setMinimumSize(640, 480)
        self.setWindowIcon(QIcon("res/icon.svg"))
        self.resize(1280, 720)
        self.terminal = Terminal(cli)
        self.setCentralWidget(self.terminal)
        self.menu = Menu()
        self.setMenuBar(self.menu)
        self.dock = Dock(cli)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.bare_commande = BarreCommande(cli)
        self.addToolBar(Qt.TopToolBarArea, self.bare_commande)
        self.bare_commande.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basedefaits)
        self.bare_commande.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basederegles)


def main_gui():
    qtTranslator = QTranslator()
    qtTranslator.load("qt_"+ QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app = QApplication(sys.argv)
    app.installTranslator(qtTranslator)
    mainwindow = FenetrePrincipal()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main_gui()