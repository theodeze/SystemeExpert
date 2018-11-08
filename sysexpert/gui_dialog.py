import os
from sysexpert import CLI, AnalyseurSyntaxique, Fait, Trace, SelectionRegle
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class Configuration(QDialog):

    def __init__(self, cli, parent=None):
        super(Configuration, self).__init__(parent)
        self.setWindowTitle("Configuration")
        self.layout = QVBoxLayout()
        self.config = QHBoxLayout()
        self.boutton = QHBoxLayout()
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
        self.config.addWidget(self.trace)

        self.regle = QGroupBox("Choix de la règle déclenchée")
        self.plus = QRadioButton(
            "Règles ayant le plus de prémisses à satisfaire")
        self.complexe = QRadioButton("Complexité d'évaluation des prémisses")
        self.premiere = QRadioButton("Premiere règle")
        self.regle_layout = QVBoxLayout()
        self.regle_layout.addWidget(self.plus)
        self.regle_layout.addWidget(self.complexe)
        self.regle_layout.addWidget(self.premiere)
        self.regle.setLayout(self.regle_layout)
        self.config.addWidget(self.regle)

        self.bc_strict = QGroupBox("Modèle de le base de connaissance")
        self.non_strict = QRadioButton("Non strict")
        self.strict = QRadioButton("Strict")
        self.bc_strict_layout = QVBoxLayout()
        self.bc_strict_layout.addWidget(self.non_strict)
        self.bc_strict_layout.addWidget(self.strict)
        self.bc_strict.setLayout(self.bc_strict_layout)
        self.config.addWidget(self.bc_strict)

        self.annuler = QPushButton("Annuler")
        self.annuler.clicked.connect(self.annule)
        self.boutton.addWidget(self.annuler)

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.valide)
        self.boutton.addWidget(self.valider)

        self.layout.addLayout(self.config)
        self.layout.addLayout(self.boutton)

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

        if self.cli.basederegles.strict:
            self.strict.setChecked(True)
        else:
            self.non_strict.setChecked(True)

    def valide(self):
        self.accept()

    def annule(self):
        self.reject()


class Aide(QDialog):

    def __init__(self, parent=None):
        super(Aide, self).__init__(parent)
        self.setWindowTitle("Aide")
        self.layout = QHBoxLayout()
        self.tabs = QTabWidget()
        self.msg_accueil = QLabel("Bienvenue dans l'aide")
        self.msg_accueil.setAlignment(Qt.AlignCenter)
        self.tabs.addTab(self.msg_accueil, "Accueil")
        self.terminal = QTextBrowser()
        self.terminal.setText(open(os.path.dirname(
            __file__) + "/res/html/aide_terminal.html", 'r').read())
        self.tabs.addTab(self.terminal, "Terminal")
        self.fichier = QTextBrowser()
        self.fichier.setText(open(os.path.dirname(
            __file__) + "/res/html/aide_fichier.html", 'r').read())
        self.tabs.addTab(self.fichier, "Fichier")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.resize(640, 480)


class APropos(QDialog):

    def __init__(self, parent=None):
        super(APropos, self).__init__(parent)
        self.setWindowTitle("A propos")
        self.layout = QVBoxLayout()
        self.texte = QLabel(open(os.path.dirname(
            __file__) + "/res/html/apropos.html", 'r').read())
        self.texte.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.texte.setOpenExternalLinks(True)
        self.layout.addWidget(self.texte)
        self.setLayout(self.layout)


class DemandeFait(QDialog):

    def __init__(self, title, parent=None):
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
