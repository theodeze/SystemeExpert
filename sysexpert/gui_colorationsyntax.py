from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class ColorationSyntax(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(ColorationSyntax, self).__init__(parent)
        self.regles = []

        motcles_format = QTextCharFormat()
        motcles_format.setForeground(QColor("#315EEE"))
        motcles_format.setFontWeight(QFont.Bold)
        # liste des mots à considérer
        motcles_motifs = [
            "TRACE",
            "LOG",
            "LIRE",
            "AFFICHER",
            "REGLE",
            "AIDE",
            "REINITIALISE",
            "DEBUG",
            "INFO",
            "BF",
            "R[0-9]+"]
        motcles_motifs += ["TRUE", "FALSE", "VRAI", "FAUX"]
        for motcles_motif in motcles_motifs:
            motcles_regex = QRegExp("\\b" + motcles_motif + "\\b",
                                    Qt.CaseInsensitive)
            self.regles.append([motcles_regex, motcles_format])

        motimp_format = QTextCharFormat()
        motimp_format.setForeground(QColor("#DA3E39"))
        motimp_format.setFontWeight(QFont.Bold)
        motimp_motifs = ["WARNING", "ERROR", "CRITICAL"]
        for motimp_motif in motimp_motifs:
            motimp_regex = QRegExp("\\b" + motimp_motif + "\\b",
                                   Qt.CaseInsensitive)
            self.regles.append([motimp_regex, motimp_format])

        operateur_format = QTextCharFormat()
        operateur_format.setForeground(QColor("#0E6FAD"))
        operateur_motif = r"[⊢:∨∧<>!≔=&\|]+"
        operateur_regex = QRegExp(operateur_motif)
        self.regles.append([operateur_regex, operateur_format])

        delimiteur_format = QTextCharFormat()
        delimiteur_format.setForeground(QColor("#0E6FAD"))
        delimiteur_motif = r"[\)\(]+|[\{\}]+|[][]+"
        delimiteur_regex = QRegExp(delimiteur_motif)
        self.regles.append([delimiteur_regex, delimiteur_format])

        nombre_format = QTextCharFormat()
        nombre_format.setForeground(QColor("#41933E"))
        nombre_motif = r"\b([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\b"
        nombre_regex = QRegExp(nombre_motif)
        self.regles.append([nombre_regex, nombre_format])

        chaine_format = QTextCharFormat()
        chaine_format.setForeground(QColor("#930092"))
        chaine_motif = '\".*\"'
        chaine_regex = QRegExp(chaine_motif)
        chaine_regex.setMinimal(True)
        self.regles.append([chaine_regex, chaine_format])

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#8E8F96"))
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


class ColorationSyntaxDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ColorationSyntaxDelegate, self).__init__(parent)
        self.document = QTextDocument(self)
        self.document.setDefaultFont(QFont("Overpass Mono", 10))
        self.coloration_syntax = ColorationSyntax(self.document)

    def drawDisplay(self, painter, option, rect, text):
        self.document.setPlainText(text)
        pixmap = QPixmap(rect.size())
        pixmap.fill(Qt.transparent)
        p = QPainter(pixmap)
        self.document.drawContents(p)
        painter.drawPixmap(rect.adjusted(-2, rect.height() / \
                           2 - 12, -2, rect.height() / 2 - 12), pixmap)
        p.end()
