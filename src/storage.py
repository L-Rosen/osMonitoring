import json , time, datetime, subprocess, scripts.sonde as sonde, scripts.get_last_cert_alert as web_parser

#On récupère le timestamp actuel et on le convertit en date
def get_date():
    timestamp = time.time()
    date = datetime.datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y_%H-%M-%S")
    return date

#On récupère les données de la sonde et du web_parser
def get_data():
    return {
        "cpu_usage": sonde.get_cpu_usage(),
        "cpu_usage_per_core": sonde.get_cpu_usage_per_core(),
        "memory_usage": sonde.get_memory_usage(),
        "storage_usage": sonde.get_storage_usage(),
        "connected_users": int(subprocess.check_output("/etc/osMonitoring/src/scripts/connected_usr.sh", shell=True, text=True).replace("\n", "")),
        "process_count": sonde.get_process_count(),
        "cert_alert": web_parser.get_cert_alert()
    }

#On stocke les données dans un fichier JSON
def json_write(date, data):
    filename = "/etc/osMonitoring/src/data/" + date + ".json"
    with open(filename, "w",encoding='utf8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)


#S'il y a plus de  100 fichiers dans le dossier data, on supprime le surplus en commençant par les plus anciens
def delete_old_files():
    subprocess.run("ls -t /etc/osMonitoring/src/data | tail -n +101 | xargs -I {} rm /etc/osMonitoring/src/data/{}", shell=True, text=True)


json_write(get_date(), get_data())
delete_old_files()