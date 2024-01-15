import bcrypt

def main():
    password = b'guest'
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)
    print(password)

    # write it to test.txt
    with open('test.txt', 'wb') as f:
        f.write(password)
    
    # read it back
    with open('test.txt', 'rb') as f:
        password = f.read()
    
    # check it
    print(bcrypt.checkpw(b'guest', password))
main()