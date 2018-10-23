# Systeme Expert

## Utilisation

```Bash
$ python3 ./main.py
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
- Ne prend pas en compte les parenthèses 
- Faire plus de test
- et encore plus