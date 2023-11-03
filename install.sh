#!/bin/bash

# Check if OS is Ubuntu or Debian
if [[ "$(uname -s)" == "Linux" ]]; then
    if [[ -f "/etc/debian_version" ]] || [[ -f "/etc/lsb-release" ]]; then
        # Install python3-tk for Ubuntu or Debian
        sudo apt-get update
        sudo apt-get install -y python3-tk
    else
        echo "Unsupported Linux distribution"
        exit 1
    fi
elif [[ "$(uname -s)" == "Darwin" ]]; then
    # Install python3-tk for macOS
    brew install python-tk
else
    echo "Unsupported operating system"
    exit 1
fi
