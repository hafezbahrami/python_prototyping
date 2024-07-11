from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import random

def iso10126_pad(data, block_size):
    pad_len = block_size - (len(data) % block_size)
    padding = bytes([random.randint(0, 255) for _ in range(pad_len - 1)]) + bytes([pad_len])
    return data + padding

def iso10126_unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt(data, key, iv):
    # Pad the data
    padded_data = iso10126_pad(data, algorithms.AES.block_size // 8)
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt(encrypted_data, key, iv):
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the data
    data = iso10126_unpad(padded_data)
    return data

# Example usage
if __name__ == "__main__":
    # Example usage
    key = os.urandom(32)  # 256-bit key for AES-256
    iv = os.urandom(16)   # 128-bit IV for AES

    data = b"Secret message!"

    # Encrypt the data
    encrypted_data = encrypt(data, key, iv)
    print("Encrypted data:", encrypted_data)

    # Decrypt the data
    decrypted_data = decrypt(encrypted_data, key, iv)
    print("Decrypted data:", decrypted_data)
