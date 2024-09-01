# Create a service file: /etc/systemd/system/edr.service

[Unit]
Description=EDR System Service

[Service]
ExecStart=/usr/bin/python3 /path/to/your/edr_script.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start the service
sudo systemctl enable edr
sudo systemctl start edr
