#!/bin/sh

sudo apt-get update
sudo apt-get install python3-pip
pip3 install pygame
pip3 install pygame_menu

LINE=21i
for music_file in sounds/*
do
    name=$(echo $music_file | awk -F/ '{print $2}' | sed 's/\.wav//g')
    var=$name\_sound_path
    grep -n "$var = " snake.py 1>/dev/null
    if [ ! $? = "0" ]
    then
        echo "Installing $music_file"
        sed -i "$LINE $var = \"$(pwd)/$music_file\"" snake.py
    fi
done

echo "Installing executable"
cat << EOF > snake.desktop
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Name=Snake Game
Exec=$(pwd)/snake.py
Icon=$(pwd)/images/snake_icon.png
EOF

mv snake.desktop $HOME/.local/share/applications/

echo "Success"
exit 0
