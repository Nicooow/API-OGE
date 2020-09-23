# -*- coding: utf-8 -*-

from oge.api import API
from getpass import getpass

api = API("nb232977", getpass(), debug=False)
api.connexion()

for m in api.getMatieres(2):
    print(f"{m.nom} : {m.nbNote} note" + "s" if m.nbNote>0 else "")

    for c in api.getCategories(m):
        print(f"    {c.nom}")

        for n in api.getNotes(c):
            print(f"        - {n.date} - {n.intitule} - {n.note}/{n.total} - coef {n.coef}")
