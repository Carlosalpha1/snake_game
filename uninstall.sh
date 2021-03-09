#!/bin/sh

for music_file in sounds/*
do
    name=$(echo $music_file | awk -F/ '{print $2}' | sed 's/\.wav//g')
    var=$name\_sound_path
    num_line=$(grep -n "$var = " snake.py | awk -F: '{print $1}')
    if [ ! $num_line = '' ]
    then
        echo "Uninstalling $music_file ..."
        sed -i "$(echo $num_line)d" snake.py
    fi
done

echo "Uninstalling executable ..."
rm $HOME/.local/share/applications/snake.desktop 2>/dev/null
