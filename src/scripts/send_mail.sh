#!/bin/bash
mail_alert=$(cat /opt/osMonitoring/src/scripts/config.cfg| grep "mail_alert" | cut -d'=' -f2)

#Mail content
mail_content="Le serveur a rencontré une ou plusieurs alertes. Voici les alertes rencontrées: \n\n"

#Récupération des données des sondes
data_file=/opt/osMonitoring/src/data/$(ls -t "/opt/osMonitoring/src/data" | head -1)

#On vérifie s'il y a une ou des alertes
result=$(bash /opt/osMonitoring/src/scripts/crisis_detection.sh)

#Si result contient 0, il a une nouvelle alerte Cert
if [[ $result == *"0"* ]]; then
    cert_link=$(grep -oP '"link": "\K[^"]+' $data_file)
    mail_content+="Nouvelle alerte Cert: $cert_link\n"
fi

#Si result contient 1, il a une alerte CPU
if [[ $result == *"1"* ]]; then
    mail_content+="Utilisation du processeur élevée.\n"
fi

#Si le résultat contient 2, il a une alerte MEM
if [[ $result == *"2"* ]]; then
    mail_content+="Utilisation mémoire élevée.\n"
fi


#On envoie un mail si le résultat n'est pas égal à "result="
if [[ $result != "result=" ]]; then
    printf "Subject: Alerte serveur\n\n$mail_content" | msmtp $mail_alert
fi