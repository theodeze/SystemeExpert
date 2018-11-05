
import sys, os
from se import Log, CLI, AnalyseurSyntaxique, ColorationSyntaxDelegate, Fait, Trace, BaseDeFaits, BaseDeRegles, SelectionRegle, Aide, DemandeFait, Configuration, APropos, Terminal
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class AffichageBaseDeConnaissance(QWidget):

    def __init__(self, cli, parent = None):
        super(AffichageBaseDeConnaissance, self).__init__(parent)
        self.cli = cli
        self.affichage_basedefaits = QTableWidget(1, 2)
        self.affichage_basedefaits.setHorizontalHeaderLabels(["Symbole","Valeur"])
        self.affichage_basedefaits.cellChanged.connect(self.modification_basedefaits)
        self.affichage_basedefaits.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.affichage_basedefaits.setFont(QFont("Overpass Mono", 10))
        self.affichage_basedefaits.setItemDelegate(ColorationSyntaxDelegate())
        self.affichage_basederegles = QListWidget()
        self.affichage_basederegles.setWrapping(True)
        self.affichage_basederegles.setFont(QFont("Overpass Mono", 10))
        self.affichage_basederegles.setItemDelegate(ColorationSyntaxDelegate())
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Base de Faits"))
        self.layout.addWidget(self.affichage_basedefaits)
        self.layout.addWidget(QLabel("Base de Règles"))
        self.layout.addWidget(self.affichage_basederegles)

        self.l1 = QHBoxLayout()
        self.bt1 = QPushButton("Ajouter règle")
        self.bt2 = QPushButton("D")
        self.l1.addWidget(self.bt1)
        self.l1.addWidget(self.bt2)
        self.layout.addLayout(self.l1)

        self.desactiver_modification = False
        self.setLayout(self.layout)

    def mise_a_jour_basedefaits(self):
        self.desactiver_modification = True
        ligne = 0
        self.affichage_basedefaits.clearContents()
        self.affichage_basedefaits.setRowCount(len(self.cli.basedefaits.pairs()) + 1)
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
                    self.cli.basedefaits.modifier(ligne, Fait(symbole, AnalyseurSyntaxique.analyse_valeur_fait(valeur)))
                else:
                    self.cli.basedefaits.ajouter(Fait(symbole, AnalyseurSyntaxique.analyse_valeur_fait(valeur)))
                    self.affichage_basedefaits.setRowCount(self.affichage_basedefaits.rowCount() + 1)
            except Exception as e:
                Log.warning(e)
                self.affichage_basedefaits.setItem(ligne, 0, QTableWidgetItem(self.cli.basedefaits.symbole(ligne)))


class Dock(QDockWidget):

    def __init__(self, cli, parent = None):
        super(Dock, self).__init__(parent)
        self.setWindowTitle("Base de connaissance")
        self.cli = cli
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.affichage_base_de_connaissance = AffichageBaseDeConnaissance(cli)
        self.setWidget(self.affichage_base_de_connaissance)

    def basculer(self):
        if self.isHidden():
            self.setHidden(False)
        else:
            self.setHidden(True)

class BarreCommande(QToolBar):
    mise_a_jour = Signal() 

    def __init__(self, cli, parent = None):
        super(BarreCommande, self).__init__(parent)
        self.cli = cli
        self.setWindowTitle("Barre de commande")
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon	)
        self.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-library_add-24px.svg"), "Charger fichier", self.charge_fichier)
        self.addSeparator()
        self.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-arrow_back-24px.svg"), "Chaînage avant", self.chainage_avant)
        self.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-arrow_forward-24px.svg"), "Chaînage arriere", self.chainage_arriere)
        self.addSeparator()
        self.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-settings-20px.svg"), "Configuration", self.configuration)
        self.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-help-24px.svg"), "Aide", self.aide)

    def basculer(self):
        if self.isHidden():
            self.setHidden(False)
        else:
            self.setHidden(True)

    def charge_fichier(self):
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
            if configuration.oui.isChecked():
                self.cli.moteur.trace = Trace.OUI
            elif configuration.non.isChecked():
                self.cli.moteur.trace = Trace.NON
            elif configuration.min.isChecked():
                self.cli.moteur.trace = Trace.MIN
            if configuration.complexe.isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.COMPLEXE
            elif configuration.premiere.isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.PREMIERE
            elif configuration.plus .isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.PLUS
            if configuration.strict.isChecked():
                self.cli.basederegles.strict = True
            else:
                self.cli.basederegles.strict = False

    def aide(self):
        aide = Aide(self)
        aide.exec()


class Menu(QMenuBar):
    mise_a_jour = Signal()
    basculer_bar = Signal()
    basculer_bdc = Signal()

    def __init__(self, cli, parent = None):
        super(Menu, self).__init__(parent)
        self.cli = cli
        self.fichier = self.addMenu("Fichier")
        self.fichier.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-library_add-24px.svg"), "Charger fichier", self.charge_fichier)
        self.fichier.addSeparator()
        self.fichier.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-settings-20px.svg"), "Configuration", self.configuration)
        self.fichier.addSeparator()
        self.fichier.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-exit_to_app-24px.svg"), "Quitter", QApplication.quit)
        self.affichage = self.addMenu("Affichage")
        self.affichage.addAction("Afficher/Cacher Barre de commande", self.basculer_bar.emit)
        self.affichage.addAction("Afficher/Cacher Base de connaisance", self.basculer_bdc.emit)
        self.basedeconnaissance = self.addMenu("Base de connaissance")
        self.basedeconnaissance.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-arrow_forward-24px.svg"), "Chaînage avant", self.chainage_avant)
        self.basedeconnaissance.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-arrow_back-24px.svg"), "Chaînage avant", self.chainage_arriere)
        self.basedeconnaissance.addSeparator()
        self.basedeconnaissance.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-clear-24px.svg"), "Réinitialiser", self.reinitialiser)
        self.aide = self.addMenu("Aide")
        self.aide.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-help-24px.svg"), "Contenu...", self.contenu)
        self.aide.addSeparator()
        self.aide.addAction(QIcon(os.path.dirname(__file__) + "/res/icons/baseline-announcement-24px.svg"), "A propos", self.apropos)

    def charge_fichier(self):
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

    def reinitialiser(self):
        self.cli.basedefaits = BaseDeFaits()
        self.cli.basederegles = BaseDeRegles()
        self.mise_a_jour.emit()

    def contenu(self):
        aide = Aide(self)
        aide.exec()

    def apropos(self):
        apropos = APropos(self)
        apropos.exec()

    def configuration(self):
        configuration = Configuration(self.cli, self)
        rep = configuration.exec()
        if rep == QDialog.Accepted:
            if configuration.oui.isChecked():
                self.cli.moteur.trace = Trace.OUI
            elif configuration.non.isChecked():
                self.cli.moteur.trace = Trace.NON
            elif configuration.min.isChecked():
                self.cli.moteur.trace = Trace.MIN
            if configuration.complexe.isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.COMPLEXE
            elif configuration.premiere.isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.PREMIERE
            elif configuration.plus .isChecked():
                self.cli.moteur.selection_regle = SelectionRegle.PLUS
            if configuration.strict.isChecked():
                self.cli.basederegles.strict = True
            else:
                self.cli.basederegles.strict = False


class FenetrePrincipal(QMainWindow):

    def __init__(self, parent = None):
        super(FenetrePrincipal, self).__init__(parent)
        cli = CLI()
        
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/res/fonts/OverpassMono-Bold.ttf")
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/res/fonts/OverpassMono-Light.ttf")
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/res/fonts/OverpassMono-Regular.ttf")
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/res/fonts/OverpassMono-SemiBold.ttf")

        self.setWindowTitle("Système Expert")
        self.setMinimumSize(640, 480)
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/res/icons/app.svg"))
        self.resize(1280, 720)
        self.terminal = Terminal(cli)
        self.setCentralWidget(self.terminal)
        self.menu = Menu(cli)
        self.setMenuBar(self.menu)
        self.dock = Dock(cli)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.bare_commande = BarreCommande(cli)
        self.addToolBar(Qt.TopToolBarArea, self.bare_commande)
        self.terminal.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basedefaits)
        self.terminal.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basederegles)
        self.menu.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basedefaits)
        self.menu.mise_a_jour.connect(self.dock.affichage_base_de_connaissance.mise_a_jour_basederegles)
        self.menu.basculer_bar.connect(self.bare_commande.basculer)
        self.menu.basculer_bdc.connect(self.dock.basculer)
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