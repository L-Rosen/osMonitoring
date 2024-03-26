# On vérifie que le le dossier data n'est pas vide
if [ -z "$(ls -A /opt/osMonitoring/src/data)" ]; then
    echo "Le dossier data est vide, il n'y a rien à sauvegarder."
    exit 1
fi

# On crée un dossier backup s'il n'existe pas
if [ ! -d "/opt/osMonitoring/src/backup" ]; then
    mkdir /opt/osMonitoring/src/backup
fi

# On crée un fichier compressé qui a pour nom la date du jour de l'execution du script
tar -czf /opt/osMonitoring/src/backup/backup-$(date +%d-%m-%Y_%H-%M-%S).tar.gz -P /opt/osMonitoring/src/data