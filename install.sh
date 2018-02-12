#!/usr/bin/env bash

zipName="simple-editor-x.zip"
binaryName="simple-editor-x"
appDirName=".simple-editor-x"

### Zip and move executable file to /usr/local/ ###
zip ${zipName} * -x venv &> /dev/null
echo '#!/usr/bin/env python' | cat - ${zipName} > ${binaryName} # adding #!/usr/bin/env python shebang to simple-editor-x file
chmod +x ${binaryName} # set execute permission

if [ ! -d ~/${appDirName} ]; then # if not exist
    mkdir ~/${appDirName}
fi

cp ${binaryName} ~/${appDirName}/${binaryName}


### move shortcut to /usr/local/bin ###
shortcutFile="sex"
chmod +x ${shortcutFile} # set execute permission
cp ${shortcutFile} /usr/local/bin/${shortcutFile}