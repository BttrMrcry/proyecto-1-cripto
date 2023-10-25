from encrypters import RSAEncrypter
import time

if __name__ == '__main__':
    encrypter = RSAEncrypter(file_path='test.txt')
    encrypter.prepare_encrypt()
    start_time = time.perf_counter()
    encrypter.encrypt()
    end_time = time.perf_counter()

    encrypter.post_encrypt()
    encrypter.prepate_decrypt()
    encrypter.decrypt()
    print(encrypter.verify())
    print(end_time-start_time)