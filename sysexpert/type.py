from enum import Enum, unique


@unique
class Operateur(Enum):
    EGALITE = "=="
    INEGALITE = "!="
    SUPERIORITE = ">"
    SUPERIORITEOUEGALITE = ">="
    INFERIORITE = "<"
    INFERIORITEOUEGALITE = "<="


@unique
class Connecteur(Enum):
    OU = "∨"
    ET = "∧"


@unique
class Parenthese(Enum):
    OUVRANT = "("
    FERMANT = ")"


@unique
class Trace(Enum):
    NON = "desactiver"
    MIN = "minimal"
    OUI = "activer"


@unique
class SelectionRegle(Enum):
    PREMIERE = "première regle"
    COMPLEXE = "complexité d'évaluation des prémisses"
    PLUS = "règles ayant le plus de prémisses à satisfaire"


class AnalyseurSimple:

    @staticmethod
    def est_fait(expression):
        if isinstance(expression, bool):
            return False
        if isinstance(expression, int):
            return False
        if isinstance(expression, float):
            return False
        if expression.startswith('"') and expression.endswith('"'):
            return False
        return True

    @staticmethod
    def valuer_expression(expression, basedefaits):
        if isinstance(expression, bool):
            return expression
        if isinstance(expression, int):
            return expression
        if isinstance(expression, float):
            return expression
        if expression.startswith('"') and expression.endswith('"'):
            return expression
        return basedefaits.valeur_fait(expression)
