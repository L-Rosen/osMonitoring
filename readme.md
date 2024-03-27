# Projet osMonitoring
## Arborescence
```
osMonitoring/
│   └── install.sh
├── README.md
├── src/
│   ├── backup/
│   │   ├── backup.sh
│   │   └── restore.sh
│   ├── scripts/
│   │   ├── config.cfg
│   │   ├── connected_usr.sh
│   │   ├── crisis_detection.sh
│   │   ├── generate_graph.py
│   │   ├── get_last_cert_alert.py
│   │   ├── send_mail.sh
│   │   ├── sonde.py
│   │   └── disk.py
│   │   └── install/
│   │       ├── install_dep.sh
│   │       ├── setup_msmtp.sh
│   │       ├── setup_config.sh
│   │       └── create_service.sh
│   └── templates/
│       └── index.html
└── web_app.py
```
## Installation
1. Cloner le projet dans le répertoire /opt/ ou copiez les fichiers manuellement dans le répertoire /opt/osMonitoring
2. Exécuter le script install.sh en tant que root pour installer les dépendances et configurer les services
3. Configurer le crontab pour lancer les scripts de monitoring et d'alerte

## Configuration du crontab
```
*/1 * * * * bash /opt/osMonitoring/src/scripts/send_mail.sh
*/1 * * * * /usr/bin/python3 /opt/osMonitoring/src/storage.py
```

L'ajout de ces lignes dans le crontab permet de lancer les scripts send_mail.sh et storage.py toutes les minutes.
Ces derniers permettent respectivement d'envoyer les mails d'alerte et de stocker les données des sondes dans la base de données.

## Vérification de l'installation
Pour vérifier que l'installation s'est bien déroulée, il suffit de se connecter sur la page web http://localhost:5000
Qui n'est autre que l'interface de monitoring. 
Pour vérifier l'état de fonctionnement du service de monitoring, il suffit de lancer la commande suivante:
```
systemctl status osMonitoring.service
```

# Installation manuelle
## Dépendances
En tant que root, exécuter les commandes suivantes pour installer les dépendances nécessaires au bon fonctionnement du service de monitoring:
```
sudo apt update
sudo apt install python3
sudo apt install python3-flask
sudo apt install python3-psutil
sudo apt install msmtp
sudo apt install python3-requests
sudo apt install python3-pygal
```

## Configuration de msmtp
Pour configurer msmtp, il suffit de modifier le fichier /etc/msmtprc en ajoutant les lignes suivantes:
```
#Valeur par defaut
defaults
auth           on
tls            on
tls_starttls	on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp

#Compte par defaut utilisant le serveur smtp de l'universite
account        univ
auth on
tls on
tls_starttls	off
host           partage.univ-avignon.fr
port           465
from           prenom.nom@alumni.univ-avignon.fr
user           prenom.nom@alumni.univ-avignon.fr
password       MOT_DE_PASSE

account default : univ
```

## Reglage des valeurs par du fichier de configuration
Pour configurer les valeurs par défaut du fichier de configuration, il suffit de modifier le fichier /opt/osMonitoring/src/scripts/config.cfg en ajoutant les lignes suivantes:
```
seuil_cpu=80.0
seuil_mem=80.0
last_alert=LAISSER_VIDE 
mail_alert=
```

Le seuil_cpu et seuil_mem correspondent respectivement aux seuils de détection de crise pour le CPU et la mémoire.
Les valeurs sont exprimées en pourcentage et doivent être au format float.

## Configuration du service
Pour configurer le service de monitoring, il suffit de modifier le fichier /etc/systemd/system/osMonitoring.service en ajoutant les lignes suivantes:
```
[Unit]
Description=Service de Monitoring

[Service]
Type=simple
 
User=root
Group=root
UMask=007
 
ExecStart=/usr/bin/python3 /opt/osMonitoring/web_app.py
 
Restart=on-failure
 
[Install]
WantedBy=multi-user.target
```

Ensuite, lancer les commandes suivantes pour activer le service:
```
sudo systemctl daemon-reload
sudo systemctl enable osMonitoring.service
sudo systemctl start osMonitoring.service
```

## Configuration du crontab
```
*/1 * * * * bash /opt/osMonitoring/src/scripts/send_mail.sh
*/1 * * * * /usr/bin/python3 /opt/osMonitoring/src/storage.py
```

L'ajout de ces lignes dans le crontab permet de lancer les scripts send_mail.sh et storage.py toutes les minutes.
Ces derniers permettent respectivement d'envoyer les mails d'alerte et de stocker les données des sondes dans la base de données.

# Fontionnement

## Collecte d'informations
Les fichiers suivants collectent les informations nécessaires au monitoring:
- sonde.py : collecte les informations sur le CPU, la mémoire, le disque, et les processus
- connected_usr.sh : collecte les informations sur les utilisateurs connectés

## Stockage et archivage:
- get_last_cert_alert.py : fichier contenant une fonction permettant de récupérer la dernière alerte et de la parser dans un format JSON
- storage.py : fichier contenant un script python utilisant les fonctions  de get_last_cert_alert.py et de sonde.py pour stocker les informations dans un fichier JSON
- backup.sh : script permettant de sauvegarder les données contenue dans le dossier data dans un fichier tar.gz
- restore.sh : script permettant de restaurer les données contenue dans le fichier tar.gz
  
## Affichage et alerte
- crisis_detection.sh : script permettant de détecter une crise en fonction des seuils définis dans le fichier de configuration
- send_mail.sh : script permettant d'envoyer un mail d'alerte en cas de crise qui utilise le script crisis_detection.sh
- generate_graph.py : fichier contenant une fonction permettant de générer un graphique à partir des données stockées dans le fichier JSON et qui renvoie un rendu utilisable par le serveur web

## Interface web
- web_app.py : fichier contenant le backend de l'interface web utilisant Flask il apelle les fonctions nécessaires pour afficher les informations sur la page web
- index.html : fichier contenant le frontend de l'interface web utilisant HTML et CSS il affiche les informations collectées par le backend , le javascript permet de rafraichir les données de la page toutes les 60 secondes