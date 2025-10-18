#!/usr/bin/env bash
# SkyScope Sentinel: Autonomous multimodal self-evolving OS-level super-agent
# Installation Script

set -e

echo "🚀 Installing SkyScope Sentinel..."

# Step 1: Install system-level dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git sqlite3 ffmpeg libsqlite3-dev chromium-browser vlc imagemagick sox -y

# Step 2: Set up Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv ~/.skyscope_sentinel_env
source ~/.skyscope_sentinel_env/bin/activate

# Step 3: Install Python packages
echo " pip installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Set up data directories
echo "🗂️  Creating data directories..."
mkdir -p ~/.sentinel_data/{memory,embeddings,media,logs,agents}
sqlite3 ~/.sentinel_data/memory/sentinel.sqlite "VACUUM;"

# Step 5: Copy application files
echo "🚚 Copying application files..."
mkdir -p ~/.skyscope_sentinel_app
cp -r skyscope_sentinel/* ~/.skyscope_sentinel_app/

# Step 6: Set up configuration
echo "⚙️  Setting up configuration..."
cp ~/.skyscope_sentinel_app/config/config.yaml.template ~/.skyscope_sentinel_app/config/config.yaml
echo "Please edit ~/.skyscope_sentinel_app/config/config.yaml to add your optional IBM Quantum API key."

# Step 7: Set up systemd service
echo "🛡️  Configuring systemd service for autostart..."
sudo bash -c 'cat > /etc/systemd/system/skyscope.service <<EOF
[Unit]
Description=SkyScope Sentinel Persistent Agent
After=network.target

[Service]
ExecStart=/home/'$USER'/.skyscope_sentinel_env/bin/python -m skyscope_sentinel.main
WorkingDirectory=/home/'$USER'/.skyscope_sentinel_app
Restart=always
User='$USER'
Environment="PYTHONPATH=/home/'$USER'/.skyscope_sentinel_app"

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable skyscope.service

echo "✅ SkyScope Sentinel installation complete!"
echo "To start the service, run: sudo systemctl start skyscope.service"
echo "To monitor the service, run: sudo journalctl -u skyscope.service -f"
echo "To interact with the agent, you will need to attach to the running process or read its logs."
echo "For manual operation, activate the venv and run: python -m skyscope_sentinel.main"