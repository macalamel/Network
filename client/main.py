"""
===================== Projet informatique 2024 ================================

nom du projet : Network


 __    __              __                                        __       
/  \\  /  |            /  |                                      /  |      
$$  \\ $$ |  ______   _$$ |_    __   __   __   ______    ______  $$ |   __ 
$$$  \\$$ | /      \\ / $$   |  /  | /  | /  | /      \\  /      \\ $$ |  /  |
$$$$  $$ |/$$$$$$  |$$$$$$/   $$ | $$ | $$ |/$$$$$$  |/$$$$$$  |$$ |_/$$/ 
$$ $$ $$ |$$    $$ |  $$ | __ $$ | $$ | $$ |$$ |  $$ |$$ |  $$/ $$   $$<  
$$ |$$$$ |$$$$$$$$/   $$ |/  |$$ \\_$$ \\_$$ |$$ \\__$$ |$$ |      $$$$$$  \\ 
$$ | $$$ |$$       |  $$  $$/ $$   $$   $$/ $$    $$/ $$ |      $$ | $$  |
$$/   $$/  $$$$$$$/    $$$$/   $$$$$/$$$$/   $$$$$$/  $$/       $$/   $$/ 
                                                                          
                                                                          
                                                                          
    
Descriptif:
    application de messagerie utilisant les socket pour communiquer.
    elle sera muni de serveur et client.
    les clients pourront communiquer entre eux via le serveur
    une interface sera réalisé si le temps le permet via le terminal
    
objectifs:
    - [OK] apprendre a manipuler les sockets
    - [OK] comprendre les relation serveur clients
    - [OK] gérer plusieurs client via le multithreading
    - [BOF] créer une interface graphique via l'invite de commande
    - [OK] gestion d'authentification

objectifs bonus:
    - [OK] implementation d'un système de chiffrement bout en bout
    - implementation d'un historique chiffré
    - possibilité d'envoyer des messages a un client non connecté
    
===============================================================================
"""


from client_V1_2 import Messagerie

if __name__=="__main__":
    app=Messagerie()
    app.run()



