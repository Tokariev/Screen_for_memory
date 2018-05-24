
#4005001610lm

import bcrypt

password = "4005001610lm".encode('utf-8')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(hashed)


hashed.find(salt)
hashed == bcrypt.hashpw(password, hashed)
print(hashed)
