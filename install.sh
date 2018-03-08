#!/usr/bin/env bash

appDirName=".simple-editor-x"

if [ ! -d ~/${appDirName} ]; then # if not exist
    mkdir ~/${appDirName}
fi

echo "copy source files to ~/${appDirName}"
cp -a . ~/${appDirName}

echo "Create a shortcut to /usr/local/bin"
shortcutFile="sex"
chmod +x ${shortcutFile} # set execute permission
cp ${shortcutFile} /usr/local/bin/${shortcutFile}

echo "Done"