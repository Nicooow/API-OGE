# API OGE

API Python permettant de récupérer automatiquement les informations sur OGE.

Lien d'OGE : https://iutdijon.u-bourgogne.fr/oge

Cette API permet de :

 - [x] Se connecter à OGE
 - [x] Récupérer les matières, catégories, et notes (note, total, coefficient)
 - [ ] Récupérer les absences
 - [ ] Récupérer les retards
 - [ ] Récupérer l'emploi du temps
 - [ ] Récupérer les informations du dossier étudiant

# Installation

Ajouter le dossier **oge** à votre projet puis importez le :

```python
from oge.api import API
```

# Exemple

`example.py`

```python
# -*- coding: utf-8 -*-

from oge.api import API
from getpass import getpass

api = API("nb232977", getpass(), debug=False)
api.connexion()

for m in api.getMatieres(1):
    print(f"{m.nom} : {m.nbNote} note" + "s" if m.nbNote>0 else "")

    for c in api.getCategories(m):
        print(f"    {c.nom}")

        for n in api.getNotes(c):
            print(f"        - {n.date} - {n.intitule} - {n.note}/{n.total} - coef {n.coef}")
```

# Documentation
## Création et connexion

```python
oge = API(utilisateur="", mdp="", debug=False):
```

`utilisateur` : nom d'utilisateur de l'UB (xx0000) (optionnel)
`mdp` : mot de passe du compte (optionnel)
`debug` : active/désactive les logs dans la console (optionnel, par défaut False)

```python
oge.connexion(utilisateur="", mdp=""):
```

`utilisateur` : nom d'utilisateur de l'UB (xx0000) (optionnel)
`mdp` : mot de passe du compte (optionnel)

**Les identifiants doivent obligatoirement être renseignés dans l'une des deux fonctions.**

## Obtention d'informations
**Matieres**
```python
api.getMatieres(semestre)
```
- `semestre` : (int) numéro du semestre voulu

retour : liste de `Matiere`

**Catégories**
```python
api.getCategories(matiere)
```
- `matiere` : (Matiere) matière pour laquelle obtenir les catégories

retour : liste de `Categorie`

**Notes**
```python
api.getNotes(categorie)
```
- `matiere` : (Categorie) catégorie pour laquelle obtenir les notes

retour : liste de `Note`

## Modèles
**Matiere**
```python
matiere = api.getMatieres(2)[0]
 ```
 - `matiere.nom` : Nom de la matière
 - `matiere.nbNote` : Nombre de note dans la matière *(-1 si introuvable)*

**Catégorie**
```python
categorie = api.getCategories(matiere)[0]
 ```
 - `categorie.nom` : Nom de la catégorie
 - `categorie.notes` : Liste des notes dans cette catégorie (objets Note)

**Note**
```python
note = api.getNotes(categorie)[0]
 ```
 - `note.date` : Nom de la matière
 - `note.intitule` : Nom de la note
 - `note.note` : Note de la note *(x/)*
 - `note.total` : Note total possible *(/x)*
 - `note.coef` : Coefficient de la note

# Screenshot
`example.py`
![example.py](https://i.imgur.com/7bWxBWE.png)
