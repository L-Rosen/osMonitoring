echo "*/1 * * * * bash /opt/osMonitoring/src/scripts/send_mail.sh" | crontab -
echo "*/1 * * * * /usr/bin/python3 /opt/osMonitoring/src/storage.py" | crontab -