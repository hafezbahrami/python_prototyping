# 0 Genreal
We have 3 type of Encryption:
- **Symmetric Encryption**: Encryption that utilizes the same key for both encryption and decryption. Anything encrypted with the key, can be decrypted with the same key. [Example](./03_symmetric_encryption.py) is provided here.
- **Asymmetric Encryption**: Keys are generated in pairs, typically a public key and private key. Anything encrypted with the public key, can only be decrypted with the private key. Used by TLS (https)
- **White-box Encryption**: Keys are hardcoded into source and compiled in a way that obfuscates them and makes the difficult to extract/find.

# 1 Symmetric Encryption

# 2 Asymmetric Encryption
[Example](./04_asymmetric_encryption.py) provided here. Points are:
- Asymmetric encryption involves two keys: a public key, which is used for encryption, and a private key, which is used for decryption.
- A common algorithm used for asymmetric encryption is RSA.

# 3 White-Boxing Encryption
White-box encryption aims to secure cryptographic keys and operations even if the attacker has full access to the system, including the implementation of the encryption algorithm itself. Implementing true white-box encryption is complex and typically involves advanced techniques beyond simple Python code. However, I can provide a very simplified example that demonstrates the concept of encrypting and decrypting data while embedding keys within the algorithm.

In this [example](./05_white_boxing_encryption.py), the key is embedded within the WhiteBoxAES class, and the AES encryption/decryption is performed using this key. This is a very simplified example and does not provide the level of security that true white-box cryptography aims to achieve, but it demonstrates the basic concept of hiding the key within the encryption algorithm.

For real-world applications and higher security, consider using established libraries and frameworks that are designed for white-box cryptography.

Points:
- **nonce** (number used once) is an arbitrary number that can only be used once in a cryptographic communication. 
- In the provided example, the nonce is included in the encrypt method because it is a critical part of the AES encryption process in EAX mode (or other modes that require a nonce, such as GCM or CTR). The nonce ensures that each encryption operation produces a unique ciphertext even if the same plaintext is encrypted multiple times with the same key. 
