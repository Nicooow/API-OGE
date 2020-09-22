# -*- coding: utf-8 -*-

from oge.api import API
from getpass import getpass

api = API("nb232977", getpass(), debug=True)
api.connexion()
