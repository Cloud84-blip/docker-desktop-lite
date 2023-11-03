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

# create dir if not exists
if [ ! -d "/usr/local/bin/docker-desktop-lite-fd" ]; then
    sudo mkdir /usr/local/bin/docker-desktop-lite-fd
fi

sudo cp -a *.py /usr/local/bin/docker-desktop-lite-fd

touch docker-desktop-lite

echo "#!/bin/bash" >> docker-desktop-lite
echo "python3 /usr/local/bin/docker-desktop-lite-fd/main.py" >> docker-desktop-lite

sudo chmod u+x docker-desktop-lite

sudo cp -a docker-desktop-lite /usr/local/bin/
sudo rm docker-desktop-lite