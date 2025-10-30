#!/bin/bash

# Setup Script for Linux/Ubuntu
# Run with: sudo bash setup_service.sh

echo "========================================"
echo "  Smart Cleaner - Linux Setup"
echo "========================================"
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "ERROR: This script must be run as sudo"
   echo "Usage: sudo bash setup_service.sh"
   exit 1
fi

# Get target folder
echo "Enter the target folder to monitor:"
echo "  Example: /home/user/test or /tmp/cleanup"
read -p "Folder path: " TARGET_FOLDER

# Validate folder
if [ ! -d "$TARGET_FOLDER" ]; then
    echo "ERROR: Folder does not exist!"
    exit 1
fi

# Get interval
read -p "Deletion interval in seconds (default 5): " INTERVAL
INTERVAL=${INTERVAL:-5}

# Get scheduled time (optional)
read -p "Scheduled time HH:MM (optional, press Enter to skip): " SCHEDULE_TIME

echo
echo "[1/3] Copying Python script to /usr/local/bin/..."
cp deleteFolderWindown_Dynamic.py /usr/local/bin/smart-cleaner
chmod +x /usr/local/bin/smart-cleaner

echo "[2/3] Creating systemd service file..."

# Create service file
cat > /etc/systemd/system/smart-cleaner.service << EOF
[Unit]
Description=Smart Cleaner - Auto Deletion Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/usr/local/bin
ExecStart=/usr/bin/python3 /usr/local/bin/smart-cleaner "$TARGET_FOLDER" $INTERVAL $SCHEDULE_TIME
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "[3/3] Enabling and starting service..."
systemctl daemon-reload
systemctl enable smart-cleaner
systemctl start smart-cleaner

echo
echo "========================================"
echo "  ✅ Setup Complete!"
echo "========================================"
echo
echo "Service Status:"
systemctl status smart-cleaner --no-pager

echo
echo "Useful Commands:"
echo "  Start service:    sudo systemctl start smart-cleaner"
echo "  Stop service:     sudo systemctl stop smart-cleaner"
echo "  Check status:     sudo systemctl status smart-cleaner"
echo "  View logs:        sudo journalctl -u smart-cleaner -f"
echo "  Disable service:  sudo systemctl disable smart-cleaner"
echo
echo "Log file location: ~/.smart-cleaner/deletion_log.txt"
echo
