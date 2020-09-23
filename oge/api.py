# -*- coding: utf-8 -*-
from oge.erreurs import *
from oge.modeles import *
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

    def getViewState(self, url):
        self.printDebug("Obtention de la clé (viewState)...")
        try:
            r = self.session.get(url)
            id = re.findall(r"<li class=\"ui-tabmenuitem(?:.*?)onclick=\"PrimeFaces\.ab\({s:&quot;(.*?)&quot;,f:(?:.*?)</li>", r.text)
            viewState = re.findall(r"id=\"javax\.faces\.ViewState\" value=\"(.*?)\" />", r.text)
        except Exception as e:
            raise ErreurReseau("Impossible d'obtenir une clé (viewState).", e)

        if(len(id)==0 or len(viewState)==0):
            raise CleIntrouvable()
        else:
            self.printDebug("Clé obtenu avec succès")
            return id[0], viewState[0]

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
                raise ErreurConnexion("Impossible de se connecter", r.status_code)

    def getMatieres(self, semestre):
        self.printDebug("Obtention des matières...")
        id, viewState = self.getViewState(self.URL_NOTE)

        dataNote = {"javax.faces.partial.execute":	"@all",
                    "javax.faces.partial.render":	"mainFormDetailNote",
                    id:	id,
                    id+"_menuid":	str(semestre-1),
                    "mainFormDetailNote_SUBMIT":	"1",
                    "javax.faces.ViewState":	viewState}

        try:
            r = self.session.post(self.URL_NOTE, data = dataNote, headers={'referer':self.URL_NOTE, 'Faces-Request': 'partial/ajax'})
        except Exception as e:
            raise ErreurReseau("Impossible d'obtenir les matieres", e)

        matieresResult = re.findall(r"request\('(.*?):elpLink',event(?:.*?)>- (.*?)</a>(?:.*?)font-style:italic;(?:.*?)\">\((?:(?:([0-9]+) note(?:s|))|(?:pas de notes))\)</font>", r.text, re.DOTALL)
        matieres = []
        for matiere in matieresResult:
            matieres.append(Matiere(matiere[0], matiere[1], matiere[2], viewState))

        self.printDebug(len(matieres), "matières obtenues ...")

        return matieres

    def getCategories(self, matiere):
        self.printDebug("Obtention des catégories et de leurs notes... (", matiere.nom,")")

        viewState = matiere.viewState
        dataNoteInfo = {"mainFormDetailNote_SUBMIT":	"1",
                        "javax.faces.ViewState":	viewState,
                        "javax.faces.behavior.event":	"click",
                        "javax.faces.partial.event":	"click",
                        "javax.faces.source":	matiere.id+":elpLink",
                        "javax.faces.partial.ajax":	"true",
                        "javax.faces.partial.execute":	matiere.id+":elpLink",
                        "mainFormDetailNote":	"mainFormDetailNote"}
        try:
            r = self.session.post(self.URL_NOTE, data = dataNoteInfo, headers={'referer':self.URL_NOTE, 'Faces-Request': 'partial/ajax'})
        except Exception as e:
            raise ErreurReseau("Impossible d'obtenir les catégories", e)

        catNotes = re.findall(r"<table(?:.*?)colspan=\"4\">(.*?)</td>(.*?)</table>", r.text, re.DOTALL)
        categories = []

        for cat in catNotes:
            categorie = Categorie(cat[0])
            notes = re.findall(r"Examen du (.*?)</td><td role=(?:.*?)\">(.*?)<(?:.*?);\">(.*?)</span>/(.*?)  </td>(?:.*?)coef\. (.*?)  </", cat[1], re.DOTALL)
            for n in notes:
                categorie.ajouterNote(n[0], n[1], n[2], n[3], n[4])
            categories.append(categorie)

        self.printDebug(len(categories), "catégories obtenues ...")
        return categories

    def getNotes(self, categorie):
        return categorie.notes
