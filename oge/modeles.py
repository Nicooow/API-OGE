# -*- coding: utf-8 -*-

class Note():
    def __init__(self, date, intitule, note, total, coef):
        self.date = date
        self.intitule = intitule
        self.note = float(note)
        self.total = float(total)
        self.coef = float(coef)

class Categorie():
    def __init__(self, nom):
        self.nom = nom
        self.notes = []

    def ajouterNote(self, date, intitule, note, total, coef):
        self.notes.append(Note(date, intitule, note, total, coef))

class Matiere():
    def __init__(self, id, nom, nbNote, viewState):
        self.id = id;
        self.nom = nom
        try:
            self.nbNote = (0 if nbNote=="" else int(nbNote))
        except ValueError:
            self.nbNote = -1
        self.categories = []
        self.viewState = viewState
