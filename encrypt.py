import getpass
from eth_account import Account
from pathlib import Path
import json


KEYSTORE_NAME = Path(".keystore.json")
def main():
    private_key = getpass.getpass("Enter your private key: ")
    my_account = Account.from_key(private_key)

    password = getpass.getpass("Enter a password: ")
    encrypted_key = my_account.encrypt(password)
    print(f"Saving to{KEYSTORE_NAME}...")
    with open(KEYSTORE_NAME, "w") as f:
        json.dump(encrypted_key, f)

if __name__ == "__main__":
    main()