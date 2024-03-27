#Installation des dépendances :
echo "Installation des dépendances..."
sudo bash /opt/osMonitoring/src/scripts/install/install_dep.sh
#Configuration de msmtp :
echo "Configuration de msmtp..."
sudo bash /opt/osMonitoring/src/scripts/install/setup_msmtp.sh
#Configuration du fichier de configuration :
echo "Configuration du fichier de configuration..."
sudo bash /opt/osMonitoring/src/scripts/install/setup_config.sh
#Création du service :
echo "Création du service..."
sudo bash /opt/osMonitoring/src/scripts/install/create_service.sh