from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import uuid
from datetime import datetime, timedelta
keysStorage = {}
def generate_rsa_key_pair():
    privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    expires = datetime.now() + timedelta(days=365)
    publicKey = privateKey.public_key()
    kid = str(uuid.uuid4())
    pemPrivate = privateKey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    pemPublic = publicKey.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    keysStorage[kid] = {"Private Key": pemPrivate, "Public Key": pemPublic, "Expiry": expires}
    return kid, pemPublic, expires
kid, publicKey, expiry = generate_rsa_key_pair()
print(f"Generated key with kid: {kid} and expiry: {expiry}")
print("Public Key:", publicKey.decode())
