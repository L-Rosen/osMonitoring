!#/bin/bash

echo "Entrez le seuil d'alerte CPU:"
read cpu

echo "Entrez le seuil d'alerte RAM:"
read ram

echo "Entrez l'email qui recevras les alertes:"
read email

echo 'Configuration du config cfg ...'
#Creation du fichier de configuration de msmtp
sudo touch /opt/osMonitoring/src/scripts/config.cfg
sudo cat > /opt/osMonitoring/src/scripts/config.cfg <<EOF
seuil_cpu=$cpu
seuil_mem=$ram
last_alert=
mail_alert=$email
EOF
echo 'Configuration du config cfg terminee'