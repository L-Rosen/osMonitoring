sudo touch /etc/systemd/system/osMonitoring.service
sudo cat > /etc/systemd/system/osMonitoring.service <<EOF
[Unit]
Description=Service de Monitoring

[Service]
Type=simple
 
User=root
Group=root
UMask=007
 
ExecStart=/usr/bin/python3 /opt/osMonitoring/web_app.py
 
Restart=on-failure
 
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable osMonitoring.service
sudo systemctl start osMonitoring.service