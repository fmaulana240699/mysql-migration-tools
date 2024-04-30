from cryptography.fernet import Fernet

# Load the secret key securely
SECRET_KEY = b'vi7GDcES2sa09t9p67PPcB89bGSGpKPiF7QRzgHClZE='

# Create an instance of the Fernet cipher
cipher_suite = Fernet(SECRET_KEY)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data


test = encrypt_data("jaringan")
print(decrypt_data(test))