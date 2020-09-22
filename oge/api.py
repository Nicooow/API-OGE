# -*- coding: utf-8 -*-
from oge.erreurs import *
import requests
import re

class API():
    URL_ACCUEIL = "http://casiut21.u-bourgogne.fr/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge%2F"
    URL_NOTE = "http://iutdijon.u-bourgogne.fr/oge/stylesheets/etu/detailsEtu.xhtml"

    def __init__(self, utilisateur="", mdp="", debug=False):
        self.utilisateur = utilisateur
        self.mdp = mdp
        self.debug = debug

        self.session = requests.session()

    def printDebug(self, *text):
        if(self.debug): print("[OGE] " + ' '.join(str(x) for x in text))


    def getKey(self, url):
        self.printDebug("Obtention de la clé...")
        try:
            keyResults = re.findall(r"name=\"execution\" value=\"(.*?)\"/>", self.session.get(url).text)
        except Exception as e:
            raise ErreurReseau("Impossible d'obtenir une clé.", e)

        if(len(keyResults)==0):
            raise CleIntrouvable()
        else:
            self.printDebug("Clé obtenu avec succès")
            return keyResults[0]

    def connexion(self, utilisateur="", mdp=""):
        self.printDebug("Connexion...")
        if(utilisateur!=""):
            self.utilisateur = utilisateur
        elif(mdp!=""):
            self.mdp = mdp

        if(self.utilisateur=="" or self.mdp==""):
            raise IdentifiantManquant('Identifiant manquant (Utilisateur ou Mot de passe)')

        try:
            r = self.session.post(self.URL_ACCUEIL, data = {'username':self.utilisateur, 'password':self.mdp, 'execution':self.getKey(self.URL_ACCUEIL), '_eventId':'submit'}, headers={'referer': self.URL_ACCUEIL})
        except Exception as e:
            raise ErreurReseau("Impossible de se connecter", e)
        else:
            self.printDebug("Code de connexion :", r.status_code)
            if(r.status_code==200):
                self.printDebug("Connexion reussi")
                return True
            else:
                raise ErreurConnexion("Impossible de se connecter, code erreur inconnue", r.status_code)
