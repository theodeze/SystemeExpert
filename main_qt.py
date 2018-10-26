
import sys
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QInputDialog, QLineEdit, QApplication, QMainWindow, QListView

from core.basedefaits import BaseDeFaits, Fait
from core.basederegles import BaseDeRegles
from core.moteurdinference import MoteurDInferance
from lecteur import Lecteur

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()

    basedefaits = BaseDeFaits()
    basederegles = BaseDeRegles()
    moteur = MoteurDInferance(True)
    lecteur = Lecteur("doc/exemple2")
    lecteur.lire_fichier(basedefaits,basederegles)

    model = QStringListModel()
    model.setStringList(basedefaits.to_array())
    listview = QListView()
    listview.setModel(model)
    ok = False
    QInputDialog().getText(mainwindow, mainwindow.tr("QInputDialog().getDouble()"),
                                   mainwindow.tr("Nom Fait:"), QLineEdit.Normals,"", ok)
    mainwindow.setCentralWidget(listview)
    mainwindow.show()
    sys.exit(app.exec_())