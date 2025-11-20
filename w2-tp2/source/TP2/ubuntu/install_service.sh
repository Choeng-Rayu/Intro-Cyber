#!/bin/bash

# Setup script for Smart Cleaner Service

echo "🔧 Installing Smart Cleaner Service..."

# Copy service file to systemd directory
sudo cp /home/choeng-rayu/academic/Year3/Intro-Cyber/w3/TP2/ubuntu/smart-cleaner.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service (auto-start on boot)
sudo systemctl enable smart-cleaner.service

# Start the service immediately
sudo systemctl start smart-cleaner.service

echo "✅ Smart Cleaner Service installed and started!"
echo ""
echo "📋 Useful commands:"
echo "   View status:    sudo systemctl status smart-cleaner"
echo "   View logs:      sudo journalctl -u smart-cleaner -f"
echo "   Stop service:   sudo systemctl stop smart-cleaner"
echo "   Start service:  sudo systemctl start smart-cleaner"
echo "   Restart service: sudo systemctl restart smart-cleaner"
echo "   Disable at boot: sudo systemctl disable smart-cleaner"
