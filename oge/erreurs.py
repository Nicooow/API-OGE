# -*- coding: utf-8 -*-

class Erreur(Exception):
    pass

class IdentifiantManquant(Erreur):
    def __init__(self, message):
        self.message = message

class CleIntrouvable(Erreur):
    def __init__(self):
        pass

class ErreurReseau(Erreur):
    def __init__(self, message, erreur):
        self.message = message
        self.erreur = erreur

class ErreurConnexion(Erreur):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
