import hashlib


def hash_data(data, algorithm):
    h = hashlib.new(algorithm)
    h.update(str(data).encode('utf-8'))
    return h.hexdigest()


def write_list_to_file(file_path, data_list):
    with open(file_path, "w") as f:
        f.write('\n'.join(map(str, data_list)) + '\n')


def read_numbers_from_file(file_path):
    with open(file_path, "r") as f:
        return [int(line) for line in f.readlines()]


def generate_hashes(salted_numbers):
    md5_hashes = [hash_data(num, 'md5') for num in salted_numbers]
    sha1_hashes = [hash_data(num, 'sha1') for num in salted_numbers]
    sha256_hashes = [hash_data(num, 'sha256') for num in salted_numbers]
    return md5_hashes, sha1_hashes, sha256_hashes


if __name__ == "__main__":
    with open("numbers.txt", "r") as f:
        numbers = read_numbers_from_file(f)

    test_salts = [1, 1000, 100000, 291673, 9999999, 30000000, 123456789, 500000000, 999999999, 100000000]

    for salt in test_salts:
        salted_numbers = [num + salt for num in numbers]
        md5_hashes, sha1_hashes, sha256_hashes = generate_hashes(salted_numbers)

        write_list_to_file(f"hashed/md5_{str(salt)}.txt", md5_hashes)
        write_list_to_file(f"hashed/sha1_{str(salt)}.txt", sha1_hashes)
        write_list_to_file(f"hashed/sha256_{str(salt)}.txt", sha256_hashes)
