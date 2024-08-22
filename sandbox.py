# Online Python - IDE, Editor, Compiler, Interpreter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii

def decrypt_password(encrypted_data, iv, hex_key):
    # Convert the 64-character hex key back to 32 bytes
    key_bytes = binascii.unhexlify(hex_key)

    # Convert the 32-character hex IV back to 16 bytes
    iv_bytes = binascii.unhexlify(iv)

    # Convert hexadecimal encrypted data back to bytes
    encrypted_data_bytes = binascii.unhexlify(encrypted_data)

    # Create the cipher object for AES-256-CBC
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data_padded = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

    # Remove padding
    padder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = padder.update(decrypted_data_padded) + padder.finalize()

    # The decrypted data is in bytes, decode it to a UTF-8 string
    return decrypted_data.decode('utf-8')

# Example usage
encrypted_data = '5a2ef79eaf27e144706ee4c437ae2869'  # Replace with the actual encrypted data
iv = '3af353b0101301873c53e3d0fd6ea1cc'  # Replace with the actual IV (32 hex characters)
hex_key = 'a542c3c016de3d76e22300ec3d0543070b553c1abf214ce6d25622773ff4142e'  # Replace with your 64-character hex key

decrypted_password = decrypt_password(encrypted_data, iv, hex_key)
print('Decrypted Password:', decrypted_password)