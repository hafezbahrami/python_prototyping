import pickle
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    return key

# Encrypt a Python object
def encrypt_object(obj, key):
    # Serialize the object into byte-stream using pickle
    serialized_obj = pickle.dumps(obj)
    
    # Create a Fernet instance with the key
    fernet = Fernet(key)
    
    # Encrypt the serialized object
    encrypted_obj = fernet.encrypt(serialized_obj)
    return encrypted_obj

# Decrypt a Python object
def decrypt_object(encrypted_obj, key):
    # Create a Fernet instance with the key
    fernet = Fernet(key)
    
    # Decrypt the encrypted object
    decrypted_data = fernet.decrypt(encrypted_obj)
    
    # Deserialize the object using pickle
    obj = pickle.loads(decrypted_data)
    return obj

# Example usage
if __name__ == "__main__":
    # Generate a key for encryption
    key = generate_key()
    
    # Original object
    original_obj = {'name': 'Alice', 'age': 30, 'city': 'Wonderland'}
    
    # Encrypt the object
    encrypted_obj = encrypt_object(original_obj, key)
    print("Encrypted object:", encrypted_obj)
    
    # Decrypt the object
    decrypted_obj = decrypt_object(encrypted_obj, key)
    print("Decrypted object:", decrypted_obj)
