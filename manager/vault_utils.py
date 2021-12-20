import itertools
from cryptography.fernet import Fernet
from generator import generate
from termcolor import cprint
from menu import create_menu
from xkcdpass import xkcd_password as xp
import hashlib
import cryptography
import yaml
import base64


# Ask for the password and set up the Fernet
def fernet_init():
    master_p = input('What is your master password?: ').encode()

    # Initialize Fernet and the key
    master_p_encoded = hashlib.sha256(master_p).digest()
    key = base64.urlsafe_b64encode(master_p_encoded)
    return Fernet(key)


def decrypt_data(f, cur_vault):
    try:
        decrypted = {f.decrypt(k).decode(): f.decrypt(v).decode() for k, v in cur_vault.items()}
        return decrypted
    except (cryptography.fernet.InvalidToken, TypeError):
        cprint('Access denied: invalid password.', 'red')
        return None


# Retrieve data from the vault
def retrieve_data():
    with open('data/vault.yaml', 'r') as vault:
        cur_vault = yaml.safe_load(vault) or {}

        # Close if empty
        if not cur_vault:
            cprint('This vault is empty.', 'red')
            vault.close()

        f = fernet_init()

        # Validate the password by decrypting the first password
        decrypted_data = decrypt_data(f, cur_vault)

        # Print out the data if everything went well
        cprint('Your vault:', 'magenta', attrs=['bold'])
        for key, value in decrypted_data.items():
            cprint('- ' + key + ': ' + value, 'magenta')

        vault.close()


# Create a new password for a service and save it to the vault
def create_new():
    f = fernet_init()

    # Update the yaml file
    with open('data/vault.yaml', 'r') as vault:
        cur_vault = yaml.safe_load(vault) or {}

        # Validate the password by decrypting the first key-value pair of the vault
        first_kv = dict(itertools.islice(cur_vault.items(), 0))
        decrypted_data = decrypt_data(f, first_kv)

        # If not authorized, close the vault and return
        if decrypted_data is None:
            vault.close()
            return

        # If everything went well, ask for the name of the service and proceed with generating a password for it
        service = f.encrypt(input('What is the name of the service you want to create a password for?: ').encode())

        # Ask whether the user wants a random password or a passphrase
        answer = create_menu('Please choose one of the options.', 'Passphrase is an alternative to a randomly generated'
                                                                  'password. It can look like this: some-random-words,'
                                                                  ' and is easier to remember so it can be easily used'
                                                                  'when you do not have a password manager by'
                                                                  'your hand.',
                             ['I want a randomly generated password', 'I want a passphrase'])

        if answer == 1:
            # Generate a random password
            password = generate()
        else:
            # Set up the xkcdpass
            wordfile = xp.locate_wordfile()
            mywords = xp.generate_wordlist(wordfile=wordfile, max_length=6)
            # Generate a passphrase
            password = xp.generate_xkcdpassword(mywords, delimiter='-', numwords=5)

        # Encrypt the password and save to the vault
        password_encrypted = f.encrypt(password.encode())
        cur_vault.update({service: password_encrypted})
        cprint('We saved your newly generated password: ' + password, 'green')

    # Save and close the vault
    with open('data/vault.yaml', 'w') as vault:
        yaml.safe_dump(cur_vault, vault)
        vault.close()
        cprint('Your vault data has been safely updated.', 'green')


def remove_password():
    f = fernet_init()
    service = input('Remove password by typing in the name of the service (ex. Twitter): ')
    # Open the vault, match the name of the service, remove it with the password, safe save
    with open('data/vault.yaml', 'r') as vault:
        cur_vault = yaml.safe_load(vault) or {}

        # Close if the vault is empty
        if not cur_vault:
            cprint('This vault is empty.', 'red')
            vault.close()
            return

        # Decrypt the data
        decrypted_data = decrypt_data(f, cur_vault)
        if decrypted_data is None:
            vault.close()
            return

        # Remove the password and the service from the vault if it exists
        if service not in decrypted_data.keys():
            cprint('No matching service found. Available options: \n' + ''.join(list(decrypted_data.keys())), 'red')
            vault.close()
            return
        else:
            # Get index of the key in the decrypted list
            key_index = list(decrypted_data.keys()).index(service)
            # Get the key from the encrypted list by using the index
            key_in_cur_vault = list(cur_vault)[key_index]
            # Delete the key-value pair
            del cur_vault[key_in_cur_vault]

    with open('data/vault.yaml', 'w') as vault:
        yaml.safe_dump(cur_vault, vault)
        vault.close()
        cprint('Service ' + service + ' removed successfully.', 'green')

    return
