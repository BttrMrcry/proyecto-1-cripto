from encrypters import RSA_OAEP
import time

if __name__ == '__main__':
    encrypter = RSA_OAEP(file_path='test.txt')
    encrypter.prepare_encrypt()
    start_time_encryption = time.perf_counter()
    encrypter.encrypt()
    end_time_decryption = time.perf_counter()
    encrypter.post_encrypt()
    encrypter.prepate_decrypt()
    start_time_decryption = time.perf_counter()
    encrypter.decrypt()
    end_time_decryption = time.perf_counter()
    print(encrypter.verify())
    print(f' Encryption time: {end_time_decryption-start_time_encryption}')
    print(f' Decryption time: {end_time_decryption-start_time_decryption}')