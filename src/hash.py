import bcrypt

def  HashPassword():
    #input a password
    #the password is transformed into a byte object because bcrypt expects bytes
    password = input().encode('utf-8')

    #generate a salt
    #rounds parameter controls computational cost (higher == slower but more secure)
    salt = bcrypt.gensalt(rounds=12)
    #hashes password using hashpw method
    #result of this is a byte object
    hashedPassword = bcrypt.hashpw(password, salt)

    print(hashedPassword)
