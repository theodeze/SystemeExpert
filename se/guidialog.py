from se import CLI, AnalyseurSyntaxique, Fait, Trace, SelectionRegle
from PySide2.QtCore import QObject, Signal, Slot, Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

class Configuration(QDialog):

    def __init__(self, cli, parent = None):
        super(Configuration, self).__init__(parent)
        self.setWindowTitle("Configuration")
        self.layout = QGridLayout()
        self.cli = cli

        self.trace = QGroupBox("Niveau de trace")
        self.non = QRadioButton("Desactiver")
        self.min = QRadioButton("Minimal")
        self.oui = QRadioButton("Activer")
        self.trace_layout = QVBoxLayout()
        self.trace_layout.addWidget(self.non)
        self.trace_layout.addWidget(self.min)
        self.trace_layout.addWidget(self.oui)
        self.trace.setLayout(self.trace_layout)
        self.layout.addWidget(self.trace, 0, 0)

        self.regle = QGroupBox("Choix de la règle déclenchée")
        self.plus = QRadioButton("Règles ayant le plus de prémisses à satisfaire")
        self.complexe = QRadioButton("Complexité d'évaluation des prémisses")
        self.premiere = QRadioButton("Premiere règle")
        self.regle_layout = QVBoxLayout()
        self.regle_layout.addWidget(self.plus)
        self.regle_layout.addWidget(self.complexe)
        self.regle_layout.addWidget(self.premiere)
        self.regle.setLayout(self.regle_layout)
        self.layout.addWidget(self.regle, 0, 1)

        self.annuler = QPushButton("Annuler")
        self.annuler.clicked.connect(self.annule)
        self.layout.addWidget(self.annuler, 1, 0)

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.valide)
        self.layout.addWidget(self.valider, 1, 1)

        self.init_boutton()
        self.setLayout(self.layout)

    def init_boutton(self):
        if self.cli.moteur.trace == Trace.NON:
            self.non.setChecked(True)
        elif self.cli.moteur.trace == Trace.MIN:
            self.min.setChecked(True)
        elif self.cli.moteur.trace == Trace.OUI:
            self.oui.setChecked(True)

        if self.cli.moteur.selection_regle == SelectionRegle.COMPLEXE:
            self.complexe.setChecked(True)
        elif self.cli.moteur.selection_regle == SelectionRegle.PLUS:
            self.plus.setChecked(True)
        elif self.cli.moteur.selection_regle == SelectionRegle.PREMIERE:
            self.premiere.setChecked(True)

    def valide(self):
        self.accept()
        
    def annule(self):
        self.reject()


class Aide(QDialog):

    def __init__(self, parent = None):
        super(Aide, self).__init__(parent)
        self.setWindowTitle("Aide")


class APropos(QDialog):

    def __init__(self, parent = None):
        super(APropos, self).__init__(parent)
        self.setWindowTitle("A propos")
        self.layout = QVBoxLayout()
        self.texte = QLabel("<h1>Système Expert</h1>\
                            <h2>Moteur d'inférence 0+</h2>\
                            <h4>Développeur (s)</h4>\
                            Théo Dézé (theo.deze@etud.univ-angers.fr) <br>\
                            Charles Mallet (charles.mallet@etud.univ-angers.fr)\
                            <h4>Lien (s)</h4>\
                            <p><a href='https://github.com/theodeze/SystemeExpert'>Github</a></p>\
                            ")
        self.texte.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.texte.setOpenExternalLinks(True)
        self.layout.addWidget(self.texte)
        self.setLayout(self.layout)



class DemandeFait(QDialog):

    def __init__(self, title, parent = None):
        super(DemandeFait, self).__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.symbole = QLineEdit()
        self.valeur = QLineEdit()
        self.boutton = QPushButton("Exécuter")
        self.boutton.clicked.connect(self.executer)
        self.layout.addWidget(QLabel("Symbole du fait"))
        self.layout.addWidget(self.symbole)
        self.layout.addWidget(QLabel("Valeur du fait"))
        self.layout.addWidget(self.valeur)
        self.layout.addWidget(self.boutton)
        self.setLayout(self.layout)

    def executer(self):
        self.accept()
