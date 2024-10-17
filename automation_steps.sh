#!/bin/bash

# Check if ansible is installed
if ! command -v ansible >/dev/null 2>&1; then
    echo "Ansible is not installed. Installing Ansible..."
    
    # Update system and install Ansible
    sudo apt update -y
    sudo apt install -y ansible
else
    echo "Ansible is already installed."
fi

# Run the Ansible playbook
echo "Running Ansible playbook to install Docker..."
ansible-playbook -i host.ini install_docker.yml
docker build -t master .
docker images ls # should fine the new image
