Arborescence :
└── osMonitoring/
    ├── README.md
    ├── src
    │   ├── backup
    │   ├── backup.sh
    │   ├── restore.sh
    │   ├── scripts
    │   │   ├── config.cfg
    │   │   ├── connected_usr.sh
    │   │   ├── crisis_detection.sh
    │   │   ├── generate_graph.py
    │   │   ├── get_last_cert_alert.py
    │   │   ├── send_mail.sh
    │   │   ├── sonde.py
    │   │   └── disk.py
    │   └── storage.py
    ├── templates
    │   └── index.html
    └── web_app.py

#Installation du projet
Pour installer le projet , il faut placer le répertoire osMonitoring dans les répertoire /opt/ de votre machine.
Ensuite, il faut installer les dépendances suivantes:
- Flask
- Psutil
- subprocess
- msmtp
- requests
- pygal

#Configuration de msmtp
Pour configurer msmtp, il faut créer un fichier msmtprc	 dans le répertoire /etc/ et y ajouter les lignes suivantes pour utiliser le serveur smtp de l'université:

account        univ
auth on
tls on
tls_starttls    off
host           partage.univ-avignon.fr
port           465
from           prenom.nom@alumni.univ-avignon.fr
user           prenom.nom@alumni.univ-avignon.fr
password       MOTDEPASSE

account default : univ

#Config.cfg
Le fichier config.cfg contient les informations de configuration des seuils d'alertes ainsi que l'email de reception des alertes Il contient les informations suivantes:
[config]
seuil_cpu= (seuil d'alerte du processeur en %)
seuil_mem= (seuil d'alerte de la mémoire en %)
last_alert= (dernière alerte cert enregistrée a laisser vide , le programme s'occupe de récupérer les infos du moteur de stockage)
mail_alert= (email de réception des alertes)
Ne pas modifier last_alert qui est utilisé pour stocker la dernière alerte cert enregistrée.

#crontab
Pour que le projet fonctionne correctement, il faut ajouter les lignes suivantes dans le fichier crontab:
*/1 * * * * bash /opt/osMonitoring/src/scripts/send_mail.sh
*/1 * * * * /usr/bin/python3 /opt/osMonitoring/src/storage.py
La première ligne permet de lancer le script qui envoie un mail s'il y a une crise détectée cela toutes les minutes.
La deuxième ligne permet de lancer le script de stockage des informations de la sonde et la récupération de la dernière alerte cert toutes les minutes.

#Lancement du projet
Il suffit de lancer web_app.py suivante:
python3 web_app.py 
Le serveur web sera lancé sur le port 5000.
On peux y accéder via l'adresse http://localhost:5000

#I. Collecte d'informations

Les fichier qui se chargent de la collecte d'informations sont les suivants:
- connected_usr.sh situé dans le répertoire /opt/osMonitoring/src/scripts
- sonde.py situé dans le répertoire /opt/osMonitoring/src/scripts

connected_usr.sh contient une commande qui permet de récupérer la liste des utilisateurs connectés à la machine. (who)

sonde.py contient des fonctions qui permettent de récupérer les informations suivantes:
- Pourcentage d'utilisation du CPU
- POurcentage d'utilisation du CPU pour chacun des coeurs
- Pourcentage d'utilisation de la mémoire
- Pourcentage d'utilisation du disque

Psutil est utilisé pour récupérer ces informations.

Ces fichiers sont pensés pour être utilisés dans d'autres affin de pouvoir utiliser ces informations dans d'autres modules, par exemple nous avons qu'a importer le fichier sonde.py dans un autre fichier pour pouvoir utiliser les fonctions de récupération d'informations.

#II. Stockage des informations et archivage
Les fichier qui se chargent du stockage des informations et de l'archivage sont les suivants:
- storage.py situé dans le répertoire /opt/osMonitoring/src
- backup.sh situé dans le répertoire /opt/osMonitoring/src
- restore.sh situé dans le répertoire /opt/osMonitoring/src

storage.py vas en premier apeller les fonctions de récupération d'informations de sonde.py et les stocker dans un fichier json puis nomer ce dernier avec la date du jour et l'heure.
Ensuite on utilise une commande pour supprimer les fichiers excédentaires , on considère que le nombre de fichier maximal de l'historique est 100.
Donc dès qu'il y a plus de 100 fichiers, on supprime les plus anciens.
Les fichiers json sont stockés dans le répertoire /opt/osMonitoring/src/data

backup.sh est un script qui permet de sauvegarder les fichiers json dans un répertoire de sauvegarde.
On utilise la commande tar pour compresser les fichiers json et les stocker dans le répertoire /opt/osMonitoring/src/backup sous un nom approprié contenant le jour et l'heure de la sauvegarde.

restore.sh est un script qui permet de restaurer les fichiers json à partir des fichiers de sauvegarde.
On supprime l'entièreté du répertoire /opt/osMonitoring/src/data puis on décompresse les fichiers de sauvegarde dans ce répertoire.

#III. Affichage et alerte
Le fichier qui se charge de la détection de crise est le suivant:
- crisis_detection.sh situé dans le répertoire /opt/osMonitoring/src/scripts

Il récupère le seuil de crise et la dernière alerte cert enregistrée dans le fichier config.cfg a l'aide d'un grep
Il récupère ensuite les dernière données stockées dans le fichier json le plus récent toujours grace a un grep.

S'il détecte une nouvelle alerte cert (donc  différente de celle enregistrée dans le fichier config.cfg) il rajoute 0 a sa variable de retour.
S'il détecte un seuil cpu dépassé, il rajoute 1 a sa variable de retour.
S'il détecte un seuil mémoire dépassé, il rajoute 2 a sa variable de retour.


Le fichier qui se charge de l'envoi de mail en cas de crise est le suivant:
- send_mail.sh situé dans le répertoire /opt/osMonitoring/src/scripts
Il a été pensé pour être utilisé avec msmtp et cron.
Il apelle le fichier crisis_detection.sh et stocke le retour de ce dernier dans une variable.
En fonction du contenu de cette dernière, il envoie un mail avec les informations de la ou les crise détectée.

Le fichier qui se charge de la génération de graphique est le suivant:
- generate_graph.py situé dans le répertoire /opt/osMonitoring/src/scripts
Il utilise la librairie pygal pour générer des graphiques en svg.
Ce dernier a été pensé pour être utilisé dans d'autres modules ,
Son fonctionnement est le suivant :
Il contient une fonction principale qui prend en argument le nombre de données a récupérer et le type de données a afficher.
Il récupère les données stockées dans les fichiers json et les stocke dans des listes.
Il génère ensuite un graphique en fonction du type de données a afficher et le nombre de données a récupérer grace a pygal.
Il retourne le code svg du graphique généré.

exemple d'utilisation:
import generate_graph as gg
gg.generate_chart("cpu_usage",10)

#IV. Interface web
Le fichier qui se charge de l'interface web est le suivant:
- web_app.py situé dans le répertoire /opt/osMonitoring
Il utilise la librairie Flask pour générer une interface web.
Il contient une route pour générer un graphique a partir du module generate_graph.py
Il contient une route pour récupérer les informations stockés dans le repertoire /opt/osMonitoring/src/data
Il contient une route pour récupérer les informations stockés dans le repertoire /opt/osMonitoring/src/backup
Il contient une route pour récupérer la dernière alerte cert enregistrée dans le dernier fichier json crée
Il contient une route pour exécuter le script de sauvegarde, une pour le script de restoration, et une pour supporimer des sauvegarde

La page web est générée a partir du fichier index.html situé dans le répertoire /opt/osMonitoring/templates
Elle contient des boutons pour exécuter les scripts de sauvegarde, de restoration et de suppression de sauvegarde.
Un conteneur pour afficher les graphiques générés a partir des données stockées dans le répertoire /opt/osMonitoring/src/data
Un formulaire pour selectionner les informations a afficher
Un tableau pour afficher les informations stockées dans le répertoire /opt/osMonitoring/src/data

Le javascript s'occupe d'uiliser les routes pour récupérer les données et les graphiques a afficher et les injecter dans la page web.
L'utilisation de jquery permet une actualisation des données sans rechargement de la page.
bootsrap est utilisé pour la mise en page de la page web.