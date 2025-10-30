import hashlib

def HashStringInput():
    
    string = input().encode('utf-8')

    sha256 = hashlib.sha256()

    sha256.update(string)

    stringHash = sha256.hexdigest()

    print(f'hash: {stringHash}')


HashStringInput()