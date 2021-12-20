from cryptography.fernet import Fernet


key = Fernet.generate_key()
f = Fernet(key)

# Create and encode the string
password = 'hello123'
password_utf = password.encode()


# Encrypt the string
encrypted_password = f.encrypt(password_utf)
print('Encrypted string: ', encrypted_password)


# Decrypt the string
decrypted_password = f.decrypt(encrypted_password)
print('Decrypted string:', decrypted_password)
