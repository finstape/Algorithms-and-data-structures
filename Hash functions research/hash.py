import hashlib

TEST_SALTS = [1, 1000, 100000, 291673, 9999999, 30000000, 123456789, 500000000, 999999999, 100000000] 

def hash_md5(data):
    h = hashlib.md5(str(data).encode('utf-8'))
    return h.hexdigest()

def hash_sha1(data):
    h = hashlib.sha1(str(data).encode('utf-8'))
    return h.hexdigest()

def hash_sha256(data):
    h = hashlib.sha256(str(data).encode('utf-8'))
    return h.hexdigest()

def write_to_file(file_path, data):
    with open(file_path, "w") as f:
        for item in data:
            f.write(str(item) + '\n')

with open("numbers.txt", "r") as f:
    NUMBERS = [int(line) for line in f.readlines()]

for salt in TEST_SALTS:
    salted_numbers = [num + salt for num in NUMBERS]
    
    MD5_HASHES = [hash_md5(num) for num in salted_numbers]
    SHA1_HASHES = [hash_sha1(num) for num in salted_numbers]
    SHA256_HASHES = [hash_sha256(num) for num in salted_numbers]

    write_to_file(f"hashed/md5_{str(salt)}.txt", MD5_HASHES)
    write_to_file(f"hashed/sha1_{str(salt)}.txt", SHA1_HASHES)
    write_to_file(f"hashed/sha256_{str(salt)}.txt", SHA256_HASHES)
