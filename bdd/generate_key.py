import os
import base64

def generate_key():
    key = os.urandom(32)  # Générer une clé de 256 bits (32 octets)
    return base64.b64encode(key).decode('utf-8')
