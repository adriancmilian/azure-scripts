import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import secrets
import subprocess

"""
secrets import is a separate .py file in the directory that is used to store the key name, 
No sensitive information is stored in the file. just the name of the keys you're trying to pull the values from.
Everything is stored in the object and is then called in a main.py file to use
"""

# Create a KeyVault object to store data to be called from main.py
class KeyVault:
    def __init__(self):
        self.pub_key = ""
        self.priv_key = ""
        self.client_id = ""
        self.cosmos = ""

# Function to get the secret and add to the objects attributes
    def get_secret(self):
        # Start powershell and authenticate to Azure account
        subprocess.run(["powershell","-Command", "connect-azaccount"])
        # Pulls the vault name from an environment varible you create
        kv_name = os.environ["KEY_VAULT_NAME"]
        kv_uri = f"https://{kv_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        # Initializes Azures Secret Client object to authenticate
        client = SecretClient(vault_url=kv_uri, credential=credential)
        # Add attributes to KeyVault object
        self.pub_key = client.get_secret(secrets.pub_name).value
        self.priv_key = client.get_secret(secrets.priv_name).value
        self.client_id = client.get_secret(secrets.client_id).value
        # Clears your Azure Session
        subprocess.run(["powershell","-Command", "disconnect-azaccount"])


