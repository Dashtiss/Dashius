# import required module
from cryptography.fernet import Fernet
import argparse
import sys
import os
from os.path import join
import colorama
from colorama import Fore

colorama.init(autoreset=True)

notAllowed = [
    ".DS_Store",
]

def encrypt(Key, File=None, Dict: str=None, Recursive: bool=False, Log: bool=False):
    """_summary_

    Args:
        Key (_type_): _description_
        File (_type_, optional): The file to encrypt. Defaults to None.
        Dict (str, optional): The dictionary. Defaults to None.
        Recursive (bool, optional): _description_. Defaults to False.
    """
    if File:
        if File in notAllowed:
            return
        if Log:
            print(f'{Fore.GREEN}[INFO] Encrypting {File}')
        with open(File, 'rb') as f:
            data = f.read()
        fernet = Fernet(Key)
        encrypted = fernet.encrypt(data)
        with open(File, 'wb') as f:
            f.write(encrypted)
        if Log:
            print(f'{Fore.GREEN}[INFO] Encrypted {File}')
    elif Dict:
        if Log:
            print(f'{Fore.GREEN}[INFO] Encrypting {Dict}')
        for file in os.listdir(Dict):
            if file in notAllowed:
                continue
            if os.path.isdir(join(Dict, file)):
                if Recursive:
                    if Log:
                        print(f'{Fore.GREEN}[INFO] Encrypting {file}')
                    encrypt(Key=Key, Dict=os.path.join(Dict, file), Recursive=Recursive, Log=Log)
                continue
            if Log:
                print(f'{Fore.GREEN}[INFO] Encrypting {file}')
            with open(join(Dict, file), 'rb') as f:
                data = f.read()
            fernet = Fernet(Key)
            encrypted = fernet.encrypt(data)
            with open(join(Dict, file), 'wb') as f:
                f.write(encrypted)
            if Log:
                print(f'{Fore.GREEN}[INFO] Encrypted {file}')
            
def decrypt(Key: str, File=None, Dict: str=None, Recursive: bool=False, Log: bool=False):
    """_summary_

    Args:
        Key (str): _description_
        File (str, optional): _description_. Defaults to None.
        Dict (str, optional): _description_. Defaults to None.
        Recursive (bool, optional): _description_. Defaults to False.
    """
    if File:
        if File in notAllowed:
            return
        if Log:
            print(f'{Fore.GREEN}[INFO] Decrypting {File}')
        with open(File, 'rb') as f:
            data = f.read()
        fernet = Fernet(Key)
        decrypted = fernet.decrypt(data)
        with open(File, 'wb') as f:
            f.write(decrypted)
    elif Dict:
        if Log:
            print(f'{Fore.GREEN}[INFO] Decrypting {Dict}')
        for file in os.listdir(Dict):
            if file in notAllowed:
                continue
            if os.path.isdir(join(Dict, file)):
                if Recursive:
                    if Log:
                        print(f'{Fore.GREEN}[INFO] Decrypting Dir {file}')
                    decrypt(Key=Key, Dict=os.path.join(Dict, file), Recursive=Recursive, Log=Log)
                continue
            if Log:
                print(f'{Fore.GREEN}[INFO] Decrypting {file}')
            with open(join(Dict, file), 'rb') as f:
                data = f.read()
            fernet = Fernet(Key)
            decrypted = fernet.decrypt(data)
            with open(join(Dict, file), 'wb') as f:
                f.write(decrypted)
            if Log:
                print(f'{Fore.GREEN}[INFO] Decrypted {file}')
    

def MainFunc():
    parser = argparse.ArgumentParser(
        prog='Virus.sh Python Version',
        description='This is a encryption script created by Dashtiss',
        epilog='Created by Dashtiss',
        add_help=True
    )
    
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-e', '--encrypt', action='store_true')
    parser.add_argument('-f', '--file', action='store', help='File to encrypt or decrypt')
    parser.add_argument('-k', '--key', action='store', help='Key to encrypt or decrypt with')
    parser.add_argument('-D', '--dict', action='store', help='Dictionary to encrypt or decrypt')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursive encrypt or decrypt')
    parser.add_argument("--log", action="store_true", help="Enable logging")
    
    args = parser.parse_args()
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    if not args.decrypt and not args.encrypt:
        print(f'{Fore.RED}[ERROR] Please specify either --decrypt or --encrypt')
        sys.exit(1)
    if args.key:
        if not os.path.exists(args.key):
            key = args.key
        else:
            with open(args.key, 'rb') as f:
                key = f.read()
            try:
                test = Fernet(key)
            except ValueError:
                print(f'{Fore.RED}[ERROR] Invalid key')
                print(f'{Fore.RED}[ERROR] Please provide a valid key')
                sys.exit(1)
    else:
        if not os.path.exists('passkey.key'):
            key = Fernet.generate_key()
            with open('passkey.key', 'wb') as f:
                f.write(key)
        else:
            with open('passkey.key', 'rb') as f:
                key = f.read()
            try:
                test = Fernet(key)
            except ValueError:
                print(f'{Fore.RED}[ERROR] Invalid key')
                print(f'{Fore.RED}[ERROR] Please provide a valid key')
                sys.exit(1)
        
    print(f'{Fore.GREEN}[INFO] Key: {key}')
    print(f"logging: {args.log}")
    if args.encrypt:
        if args.file:
            encrypt(Key=key, File=args.file, Log=args.log)
        elif args.dict:
            encrypt(Key=key, Dict=args.dict, Recursive=args.recursive, Log=args.log)
    elif args.decrypt:
        if args.file:
            decrypt(Key=key, File=args.file, Log=args.log)
        elif args.dict:
            decrypt(Key=key, Dict=args.dict, Recursive=args.recursive, Log=args.log)

MainFunc()