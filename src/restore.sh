#Si le dossier backup est vide, on ne peut pas restaurer
if [ -z "$(ls -A /opt/osMonitoring/src/backup)" ]; then
        echo "Rien à restaurer, le dossier backup est vide."
        exit 1
fi

#Si le dossier data n'est pas vide, on le vide
if [ ! -z "$(ls -A /opt/osMonitoring/src/data)" ]; then
    rm -r /opt/osMonitoring/src/data/*
fi

#Si aucun argument n'est passé, on décompresse le fichier le plus récent
if [ -z $1 ]; then
    #On supprime le contenu du dossier data et on décompresse le fichier le plus récent
    tar -xzf "/opt/osMonitoring/src/backup/"$(ls -t /opt/osMonitoring/src/backup/ | head -1)
else
    #On décompresse le fichier passé en argument
    tar -xzf /opt/osMonitoring/src/backup/$1 -C /opt/osMonitoring/src/ -P
fi