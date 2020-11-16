from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def Save_keys():
    # генерируем закрытый ключ
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=4096, backend=default_backend())
    
    # вытаскиваем открытый ключ из закрытого ключа
    public_key = private_key.public_key()
    
    # сохраняем закрытый ключ   
    pem_priv = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    with open('private_key.pem', 'wb') as pem_out:
        pem_out.write(pem_priv)     
    
    # сохраняем открытый ключ
    pem_pub = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)    
    with open("public_key.pem", "wb") as file:  
        file.write(pem_pub)
    

def Encrypt(message):
    
    with open("public_key.pem", "rb") as file:
        pemlines = file.read()
        
    public_key = load_pem_public_key(pemlines, default_backend())
    
    cipher_text = public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))      
    
    return cipher_text

def Decrypt(cipher_text):
    
    with open('private_key.pem', 'rb') as file:
        pemlines = file.read()
        
    private_key = load_pem_private_key(pemlines, None, default_backend())
     
    plain_text = private_key.decrypt(cipher_text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    
    return plain_text

