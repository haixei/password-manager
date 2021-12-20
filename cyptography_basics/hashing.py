import bcrypt

# Encode the password
password = 'bye123'
password_utf = password.encode()

# Hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password_utf, salt)

print('Hashed password:', hashed_password)


# Compare password input to the correct password
def validate_password(password_to_check, valid_hashed_password):
    password_to_check = password_to_check.encode()
    valid_hashed_password = valid_hashed_password.encode()
    return bcrypt.hashpw(password_to_check, valid_hashed_password) == valid_hashed_password


is_valid_corr = validate_password('bye123', hashed_password)
print('Can login with the correct password:', is_valid_corr)
