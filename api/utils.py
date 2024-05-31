import base64
from models import SessionLocal
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import repository as repository

db = SessionLocal()

def encrypt_data(data):
    """
    Chiffre les données spécifiées avec la clé symétrique stockée dans la base de données.
    """
    try:
        key = repository.get_symmetric_key(db)
        if not key:
            raise Exception("Aucune clé symétrique n'a été trouvée dans la base de données.")
        
        key = base64.b64decode(key)  # Convertir la clé de base64 en bytes
        
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())  # Initialiser le chiffrement AES-ECB
        
        padder = padding.PKCS7(algorithms.AES.block_size).padder()  # Ajouter du padding pour garantir que la taille est un multiple de la taille de bloc
        
        # Convertir les données en chaîne de caractères avant de les encoder
        data_str = str(data)
        padded_data = padder.update(data_str.encode()) + padder.finalize()
        
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()  # Chiffrer les données
        
        return base64.b64encode(ciphertext).decode('utf-8')  # Encodage en base64 pour stockage
    except Exception as e:
        print(f"Erreur lors du chiffrement des données : {e}")
        raise e
    

def decrypt_data(data):
    """
    Déchiffre les données spécifiées avec la clé symétrique stockée dans la base de données.
    """
    try:
        key = repository.get_symmetric_key(db)
        if not key:
            raise Exception("Aucune clé symétrique n'a été trouvée dans la base de données.")
        
        key = base64.b64decode(key)  # Convertir la clé de base64 en bytes
        
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())  # Initialiser le chiffrement AES-ECB
        
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(base64.b64decode(data)) + decryptor.finalize()  # Déchiffrer les données
        
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()  # Retirer le padding
        
        # Convertir les données déchiffrées de bytes en chaîne, puis en entier
        return int(plaintext.decode('utf-8'))
    except Exception as e:
        print(f"Erreur lors du déchiffrement des données : {e}")
        raise e
