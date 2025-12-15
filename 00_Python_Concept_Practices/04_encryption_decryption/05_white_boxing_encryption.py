from Crypto.Cipher import AES
import os

class WhiteBoxAES:
    def __init__(self, key):
        # Embed the key in the class itself
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_EAX)

    def encrypt(self, plaintext):
        # Encrypt the plaintext
        nonce = self.cipher.nonce                                   # nonce (number used once) is an arbitrary number that can only be used once in a cryptographic communication. 
        ciphertext, tag = self.cipher.encrypt_and_digest(plaintext)
        return nonce, ciphertext, tag

    def decrypt(self, nonce, ciphertext, tag):
        # Decrypt the ciphertext
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext

# Example usage
key = os.urandom(16)  # Generate a random key
wb_aes = WhiteBoxAES(key)

plaintext = b'Hello, world!'
nonce, ciphertext, tag = wb_aes.encrypt(plaintext)
print(f'Ciphertext: {ciphertext}')

decrypted_text = wb_aes.decrypt(nonce, ciphertext, tag)
print(f'Decrypted text: {decrypted_text}')
