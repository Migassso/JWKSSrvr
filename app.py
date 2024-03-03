from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from keyManager import generate_rsa_key_pair, keysStorage
import jwt
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
app = Flask(__name__)
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    non_expired_keys = []
    for kid, key_info in keysStorage.items():
        if key_info["Expiry"] > datetime.now():
            # Deserialize the PEM-encoded public key
            public_key = serialization.load_pem_public_key(
                key_info["Public Key"],
                backend=default_backend()
            )
            if isinstance(public_key, rsa.RSAPublicKey):
                public_numbers = public_key.public_numbers()
                modulus = public_numbers.n
                exponent = public_numbers.e
                jwk = {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": kid,
                    "alg": "RS256",
                    "n": base64.urlsafe_b64encode(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).rstrip(b'=').decode('utf-8'),
                    "e": base64.urlsafe_b64encode(exponent.to_bytes((exponent.bit_length() + 7) // 8, byteorder='big')).rstrip(b'=').decode('utf-8'),
                }
                non_expired_keys.append(jwk)   
    return jsonify({"keys": non_expired_keys})
@app.route("/auth", methods=["POST"])
def auth():
    use_expired_key = "expired" in request.args
    for kid, key_info in keysStorage.items():
        if (use_expired_key and key_info["Expiry"] <= datetime.now()) or (not use_expired_key and key_info["Expiry"] > datetime.now()):
            private_key = key_info["Private Key"]
            payload = {
                "iss": "~~~migasso~~~",
                "exp": datetime.utcnow() + timedelta(minutes=5),  # 5 minutes expiration
            }
            token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})
            return jsonify({"token": token})
    return jsonify({"error": "No suitable key found"}), 400
if __name__ == "__main__":
    app.run(port=8080)