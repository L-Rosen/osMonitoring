import pygal
import json
import os
from pygal import Config

data_folder = "/opt/osMonitoring/src/data"

def generate_chart(request,nb):
    nb = int(nb)
    #cpu_usage  ,cpu_usage_per_core ,memory_usage ,storage_usage ,process_count, connected_users
    cpu_usage = []
    cpu_usage_per_core = []
    memory_usage = []
    storage_usage = []
    process_count = []
    connected_users = []
    date = []

    #On récupère la liste des fichiers json dans le fichier data dans l'order chronologique grâce à os.listdir
    liste = os.listdir(data_folder)
    liste.sort()

    #On retire les nb premiers éléments de la liste
    liste = liste[-nb:]
        
    for element in liste:
        with open(data_folder+"/"+element) as f:
            match request:
                case "cpu_usage":
                    cpu_usage.append(json.load(f)["cpu_usage"])
                case "cpu_usage_per_core":
                    cpu_usage_per_core.append(json.load(f)["cpu_usage_per_core"])
                case "memory_usage":
                    memory_usage.append(json.load(f)["memory_usage"])
                case "storage_usage":
                    storage_usage.append(json.load(f)["storage_usage"])
                case "process_count":
                    process_count.append(json.load(f)["process_count"])
                case "connected_users":
                    connected_users.append(json.load(f)["connected_users"])
                case _:
                    print("Erreur argument invalide, veuillez réessayer")
                    exit(1)
            date.append(element.split("_")[1].split(".")[0].replace("-", ":")+" "+element.split(".")[0].split("_")[0].replace("-", "/"))

    match request:
        case "cpu_usage":
            #Configuration du graphique
            config = Config()
            config.show_legend = False
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Pourcentage d\'utilisation CPU'
            
            #Création du graphique
            line_chart = pygal.Line(config)
            line_chart.add('Charge CPU', cpu_usage)
            return line_chart.render(is_unicode=True)

        case "cpu_usage_per_core":
            #Configuration du graphique
            config = Config()
            config.legend_at_bottom = True
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Pourcentage d\'utilisation CPU pour chaque coeur'
            
            #Création du graphique
            bar_chart = pygal.StackedBar(config)
            for i in range(len(cpu_usage_per_core[0])):
                bar_chart.add('Coeur '+str(i), [cpu_usage_per_core[j][i] for j in range(len(cpu_usage_per_core))])
            return bar_chart.render(is_unicode=True)

        case "memory_usage":
            #Configuration du graphique
            config = Config()
            config.show_legend = False
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Pourcentage d\'utilisation mémoire'
            
            #Création du graphique
            line_chart = pygal.Line(config)
            line_chart.add('Charge mémoire', memory_usage)
            return line_chart.render(is_unicode=True)
        
        case "storage_usage":
            #Configuration du graphique
            config = Config()
            config.show_legend = False
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Pourcentage d\'utilisation du stockage'
            
            #Création du graphique
            line_chart = pygal.Line(config)
            line_chart.add('Charge stockage', storage_usage)
            return line_chart.render(is_unicode=True)
        
        case "connected_users":
            #Configuration du graphique
            config = Config()
            config.show_legend = False
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Nombre d\'utilisateurs connectés'
            
            #Création du graphique
            line_chart = pygal.Line(config)
            line_chart.add('Nombre d\'utilisateurs connectés', connected_users)
            return line_chart.render(is_unicode=True)
        
        case "process_count":
            #Configuration du graphique
            config = Config()
            config.show_legend = False
            config.x_label_rotation = 20
            if nb > 0 and nb <= 30:
                config.x_labels = date
            config.title = 'Nombre de processus'
            
            #Création du graphique
            line_chart = pygal.Line(config)
            line_chart.add('Nombre de processus', process_count)
            return line_chart.render(is_unicode=True)