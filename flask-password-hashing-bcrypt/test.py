from bcrypt import hashpw, checkpw, gensalt

hashed_password = hashpw('foobar'.encode('utf-8'), gensalt())

print(checkpw('foobar'.encode('utf-8'), hashed_password)) # prints True
print(checkpw('foobarbaz'.encode('utf-8'), hashed_password)) # prints False