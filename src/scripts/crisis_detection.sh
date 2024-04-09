result="result="

# Récupération des valeurs seuils et de la dernière alerte
seuil_cpu=$(cat /opt/osMonitoring/src/scripts/config.cfg | grep "seuil_cpu" | cut -d'=' -f2)
seuil_mem=$(cat /opt/osMonitoring/src/scripts/config.cfg| grep "seuil_mem" | cut -d'=' -f2)
last_alert=$(cat /opt/osMonitoring/src/scripts/config.cfg | grep "last_alert" | cut -d'=' -f2)

# On vérifie que le dossier data n'est pas vide
if [ -z "$(ls -A /opt/osMonitoring/src/data)" ]; then
    exit 1
fi

data_file=/opt/osMonitoring/src/data/$(ls -t "/opt/osMonitoring/src/data" | head -1)

# Utilise grep pour extraire les valeurs cpu_usage, memory_usage et storage_usage du fichier json le plus récent
cpu_usage=$(grep -oP '"cpu_usage": \K[0-9.]+' "$data_file")
memory_usage=$(grep -oP '"memory_usage": \K[0-9.]+' "$data_file")
cert_alert=$(grep -oP '"title": "\K[^"]+' "/opt/osMonitoring/src/data/CERT.json")

if [[ "$last_alert" != "$cert_alert" ]]; then
    result+="0"
    sed -i "s|last_alert=$last_alert|last_alert=$cert_alert|" /opt/osMonitoring/src/scripts/config.cfg
fi

if (( $(echo "$cpu_usage > $seuil_cpu" | bc -l) )); then
    result+="1"
fi

if (( $(echo "$memory_usage > $seuil_mem" | bc -l) )); then
    result+="2"
fi

echo "$result"
