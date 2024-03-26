#Module python importable plus tard
import psutil

#Fonction qui retourne la charge CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

#Fonction qui retourne un array avec la charge CPU de chaque coeur
def get_cpu_usage_per_core():
    return psutil.cpu_percent(interval=0.1, percpu=True)

#Fonction qui retourne le pourcentage de mémoire utilisée
def get_memory_usage():
    return psutil.virtual_memory().percent

#Fonction qui retourne le pourcentage de stockage utilisé
def get_storage_usage():
    return psutil.disk_usage("/").percent

#Fonction qui retourne le nombre de processus en cours
def get_process_count():
    return len(psutil.pids())

