
from src.scripts.generate_graph import generate_chart
from flask import Flask, render_template, send_from_directory, jsonify
import subprocess, os, json, src.scripts.get_last_cert_alert as web_parser



app = Flask(__name__)
data_folder = "/opt/osMonitoring/src/data"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    all_data = []
    #On récupère la liste des fichiers json dans le fichier data dans l'order chronologique grâce à os.listdir
    liste = os.listdir(data_folder)
    liste.sort()
    liste.reverse()

    for element in liste:
        if element.endswith(".json"):
            with open(data_folder+"/"+element) as f:
                data = json.load(f)
                data["Date"] = element.split("_")[1].split(".")[0].replace("-", ":")+" "+element.split(".")[0].split("_")[0].replace("-", "/")
                del data["cert_alert"]
                #On remplace les nom des clés par des noms plus explicites pour l'utilisateur
                data["Utilisation CPU"] = data.pop("cpu_usage")
                data["Utilisation CPU par coeur"] = data.pop("cpu_usage_per_core")
                data["Utilisation mémoire"] = data.pop("memory_usage")
                data["Utilisation stockage"] = data.pop("storage_usage")
                data["Nombre de processus"] = data.pop("process_count")
                data["Nombre d'utilisateurs connectés"] = data.pop("connected_users")

                all_data.append(data)
    return jsonify(all_data)

#On genère le graphique demandé
@app.route('/get_graph/<request>/<nb>')
def get_graph(request, nb):
    return generate_chart(request, nb)

#On récupère la dernière alerte cert
@app.route('/get_cert_alert')
def get_cert_alert():
    return jsonify(web_parser.get_cert_alert())

#On renvoie le contenu du dossier backup sous forme d'un json, on utilise \n comme séparateur
@app.route('/get_backup_folder_content')
def get_backup_folder_content():
    return jsonify(subprocess.check_output("ls /opt/osMonitoring/src/backup", shell=True, text=True).replace("\n", " ").split())

#On exécute le script de backup
@app.route('/backup')
def backup():
    os.system("bash /opt/osMonitoring/src/backup.sh")
    return "Backup effectué"

#On exécute le script de restauration
@app.route('/restore/<filename>')
def restore(filename):
    os.system("bash /opt/osMonitoring/src/restore.sh " + filename)
    return "Restauration effectuée"
        
@app.route('/delete_backup/<filename>')
def delete_backup(filename):
    os.system("rm /opt/osMonitoring/src/backup/" + filename)
    return "Backup supprimé"

if __name__ == '__main__':
    app.run(debug=True)


