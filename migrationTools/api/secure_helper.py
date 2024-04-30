from cryptography.fernet import Fernet

# Load the secret key securely
SECRET_KEY = 'vi7GDcES2sa09t9p67PPcB89bGSGpKPiF7QRzgHClZE='

# Create an instance of the Fernet cipher
cipher_suite = Fernet(SECRET_KEY)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    encrypted_data_str = encrypted_data.decode('utf-8')
    return encrypted_data_str

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data