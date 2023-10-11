#!/bin/bash

sudo apt -y update
sudo apt upgrade
sudo apt -y install git build-essential python3-dev python3-pip python3-venv python-dbus cmake clang brightnessctl

########
# Font #
########
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Mononoki.zip
unzip Mononoki.zip -d ~/.fonts
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/UbuntuMono.zip
unzip UbuntuMono.zip -d ~/.fonts
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip
unzip FiraCode.zip -d ~/.fonts
fc-cache -fv

#######
# ZSH #
#######
sudo apt install zsh
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

#########
# i3 #
#########
sudo apt install i3 polybar

#############
# ALACRITTY #
#############
sudo apt install wget apt-transport-https gnupg2 software-properties-common
sudo add-apt-repository ppa:aslatter/ppa
sudo apt update
sudo apt install alacritty
sudo apt -y install npm
sudo npm i -g alacritty-themes
alacritty-themes --create

#########
# PiCom #
#########
sudo apt install libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev libpcre2-dev libpcre3-dev libevdev-dev uthash-dev libev-dev libx11-xcb-dev meson

git clone https://github.com/yshui/picom.git
cd picom
git submodule update --init --recursive
meson --buildtype=release . build
ninja -C build
sudo ninja -C build install

###############
# Lock-screen #
###############
sudo apt -y install imagemagick autoconf gcc make pkg-config libpam0g-dev libcairo2-dev libfontconfig1-dev libxcb-composite0-dev libev-dev libx11-xcb-dev libxcb-xkb-dev libxcb-xinerama0-dev libxcb-randr0-dev libxcb-image0-dev libxcb-util-dev libxcb-xrm-dev libxcb-xtest0-dev libxkbcommon-dev libxkbcommon-x11-dev libjpeg-dev
git clone https://github.com/Raymo111/i3lock-color.git
cd i3lock-color
./install-i3lock-color.sh

wget https://github.com/pavanjadhaw/betterlockscreen/archive/refs/heads/main.zip
unzip main.zip

cd betterlockscreen-main/
chmod u+x betterlockscreen
sudo cp betterlockscreen /usr/local/bin/

sudo cp system/betterlockscreen@.service /usr/lib/systemd/system/
sudo systemctl enable betterlockscreen@$USER

betterlockscreen -u $HOME/.wallpapers

#########
# UTILS #
#########
# Utils
sudo apt install rofi feh ranger htop neofetch qutebrowser autorandr arandr gedit bat
pip install numpy matplotlib scipy sympy tqdm pqdm pandas tabulate pyyaml psutil escrotum dbus-next
cargo install exa 

# Snap
sudo rm /etc/apt/preferences.d/nosnap.pref
sudo apt update
sudo apt install snapd
# Telegram
sudo snap install telegram-desktop 
# Spotify
sudo snap install spotify 
# VS code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt install apt-transport-https
sudo apt update
sudo apt install code
