# Projet Demineur

Notre projet de démineur en Python est une application utilisant les bibliothèques de Tkinter pour l’interface utilisateur ainsi que les modules socket et threading qui offrent la possibilité d’une expérience en ligne. 

Le démineur est un jeu se jouant sur une grille de cases. Plusieurs cases contiennent des mines, le but du joueur est de découvrir toutes les cases sans mines en localisant celles contenant les mines. Lorsque le joueur clique sur une case, celle-ci est “découverte” et affiche le nombre de mines situées autour d’elle. Dans l’optique d’une meilleure jouabilité, nous avons veillé à ce que la première case sur laquelle on clique ne contienne pas de mine ni de mine autour. Notre démineur comporte une particularité, il se joue en multijoueur. Deux joueurs peuvent jouer sur une même grille. Ils se connectent au serveur avec leur ip et un port, puis choisissent un pseudo. Ils jouent chacun leur tour et ont 10 secondes par tour. Le joueur qui clique sur une mine en premier perd la partie. Si toute la grille est découverte, il y a égalité entre les deux joueurs. Le code à d’abord été écrit en procédural, nous l’avons transformé en orienté objet lors de l’implémentation réseaux. Nous avons utilisé Github pour collaborer sur le code du jeu, Git nous a servi au versionning, nécessaire à la collaboration. Nous avons utilisé la librairie Pyinstaller afin de compiler le client en .exe.



## Installation

Ouvrir les fichiers NSI_client.py et server.py dans spyder. Ensuite, ouvrir 3 consoles distinctes sur spyder en faisant un clique droit sur l'onglet de consol. Lancer enfin une instance du server dans une console et lancer deux instance sur deux consoles DIFFERENTES des clients.
