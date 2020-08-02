from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash('foobar')

print(check_password_hash(hashed_password, 'foobar')) # prints True
print(check_password_hash(hashed_password, 'foobarbaz')) # prints False