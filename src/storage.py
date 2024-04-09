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
        "connected_users": int(subprocess.check_output("/opt/osMonitoring/src/scripts/connected_usr.sh", shell=True, text=True).replace("\n", "")),
        "process_count": sonde.get_process_count()
    }

#On stocke les données dans un fichier JSON
def json_write(date, data):
    filename = "/opt/osMonitoring/src/data/" + date + ".json"
    with open(filename, "w",encoding='utf8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

#On remplace le fichier CERT.json par un fichier contenant la dernière alerte de certificat uniquement si elle est différente
def update_cert_alert():
    #Si le fichier CERT.json existe
    if subprocess.run("test -f /opt/osMonitoring/src/data/CERT.json", shell=True).returncode == 0:
        with open("/opt/osMonitoring/src/data/CERT.json", "r") as file:
            old_cert_alert = json.load(file)
            new_cert_alert = web_parser.get_cert_alert()
            #Si la nouvelle alerte est différente de l'ancienne
            if old_cert_alert.get("title") != new_cert_alert.get("title"):
                with open("/opt/osMonitoring/src/data/CERT.json", "w") as file:
                    json.dump(new_cert_alert, file,ensure_ascii=False, indent=4) 

    #Si le fichier CERT.json n'existe pas
    else:
        new_cert_alert = web_parser.get_cert_alert()
        with open("/opt/osMonitoring/src/data/CERT.json", "w") as file:
            json.dump(new_cert_alert, file,ensure_ascii=False, indent=4)
        

#S'il y a plus de  100 fichiers dans le dossier data, on supprime le surplus en commençant par les plus anciens en ignonrant le fichier CERT.json
def delete_old_files():
    files = subprocess.check_output("ls -t /opt/osMonitoring/src/data", shell=True, text=True).split("\n")
    if len(files) > 100:
        for file in files[100:]:
            if file != "CERT.json" and file != "":
                subprocess.run("rm /opt/osMonitoring/src/data/" + file, shell=True)

update_cert_alert()
json_write(get_date(), get_data())
delete_old_files()