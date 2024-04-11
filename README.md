# Network

Network est une application de messagerie sécurisée

## Fonctionnalités
- **Gestion des clés :** Le système gère automatiquement la génération, la distribution des clés de chiffrement pour assurer la sécurité des communications.
- **Gestion de plusieurs clients :** Utilisation du multithreading pour connecter plusieurs clients
- **Autentification securisée :** Utilisation du RSA et du Vigenère pour securiser l'envoie du mot de passe
- **Discussion en clair :** Par default la discussion est en claire avec tous les utlisateurs
- **Listage des utilisateur :** La commande `! list user` permet d'afficher la liste des utilisateurs connecté
- **Tunnel chiffré :** Possibilité de connecter plusieurs utilisateurs via un tunnel chiffré avec la commande `!make tunnel,[user1],[user2]`
## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Lancez le serveur avec serveur\main.py
3. lancez le client avec client\main.py
4. vous pouvez changer l"adresse IP du serveur dans le code du main.py en ajoutant un paramètre dans la classe Messagerie
5. **ATTENTION** il faut aussi chager les IP des clients si vous modifier celle du serveur

## Technologies utilisées
- **codé en python**
- **modules** :
  - *socket*
  - *sys*
  - *csv*
  - *os*
  - *time*
  - *threading*
  - *hashlib*
  - *random*
- **chiffrement** :
  - *RSA*
  - *Vigenère*

## Auteurs
([@Wallaby](https://github.com/macalamel))

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
