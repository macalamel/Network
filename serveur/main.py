"""
serveur programme créé le 25/01/2024

auteur Martin Calamel
"""

from Serveur_2_2 import Messagerie,Authentification

if __name__=="__main__":
    app=Messagerie()
    app.run()

# if __name__=="__main__":
#     print(Authentification("martin2","password").connect())