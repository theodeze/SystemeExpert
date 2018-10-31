# Systeme Expert

## Sujet

### 1) Implémentation de différentes stratégies d'exploitation des règles:
- [x] Chaînage avant
- [x] Chaînage arriêre 

### 2) Utilisation de différents critères de choix de la règle déclenchée dans l'ensemble des conflits (ie. Ensemble des règles déclenchable ou susceptible d'être choisies pour développer un but):
- [x] complexité d'évaluation des prémisses
- [x] règles ayant le plus de prémisses à satisfaire
- [ ] récence d'utilisation de la règle
- [ ] règle comportant comme prémisses les faits déduits le plus récents

### 3) Possibilité de fournir des explications:
- [ ] à la demande de l'utilisateur
- [ ] en cas de problème
- [x] explication sous forme de trace
- [x] explication sous forme de trace abrégées

### 4) Gestion de la cohérence. Vous définirez des critères définissant la cohérence de la base de connaissance (définition d'un modèle de cohérence ou C-modèle) et les utiliserez pour contrôler la base de connsissance et le fonctionnement du système.



## Installation

```Bash
$ python setup.py install --user
$ systemeexpert
```

## Utilisation

```Bash
$ python run.py ou systemeexpert si installé
```

## Syntaxe du fichier de Base de connaissance

Modélisation d'un fait:

```
<Attribut> = <Valeur>
#Exemple
A = True
B = 40
```

Modélisation d'une rêgle:

```
<Fait> (& <Fait>) := <Prémisses> (& ou || <Prémisses>)
#Exemple
C = True & D = False := A == True || B > 50
D = True := A == False & B <= 50
```

Des exemples de Base de connaissance ce trouve dans le dossier doc.

## A faire
- probleme opérateur exemple (ex: 4 < b)
- aide 
- Faire plus de test
- et encore plus