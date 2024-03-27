!#/bin/bash

#Script qui demande les infos a l'utilisateur pour configurer msmtp
#et qui configure le fichier de configuration de msmtp

echo "Entrez votre prenom:"
read prenom

echo "Entrez votre nom:"
read nom

echo "Entrez votre mot de passe:"
stty -echo
read MOTDEPASSE
stty echo

echo 'Configuration de msmtp en cours...'
#Creation du fichier de configuration de msmtp
sudo touch /etc/msmtprc
sudo cat > /etc/msmtprc <<EOF
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
from           $prenom.$nom@alumni.univ-avignon.fr
user           $prenom.$nom@alumni.univ-avignon.fr
password       $MOTDEPASSE

account default : univ
EOF
echo 'Configuration de msmtp terminee'