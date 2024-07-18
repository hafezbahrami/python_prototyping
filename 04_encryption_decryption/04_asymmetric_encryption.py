from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate RSA keys: RSA keys are generated using the rsa.generate_private_key method. The public_exponent and key_size parameters define the properties of the RSA keys.
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Serialize keys to PEM format: The generated keys are serialized to PEM format. This step is optional but often useful for storing or sharing keys.
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# The public key is used to encrypt the message. The padding.OAEP scheme with SHA-256 is used for padding.
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Print keys
print(f"\n Private Key:\n{private_pem.decode()}")
print(f"\n Public Key:\n{public_pem.decode()}")

# Encrypt a message
message = b'Hello, world!'
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(f"\n Ciphertext: {ciphertext}")

# Decrypt the message
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(f"\n Decrypted text: {plaintext}")
