import abc, os, struct
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Encrypter(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def encrypt(self) -> None:
        pass
    @abc.abstractmethod
    def decrypt(self) -> None:
        pass
    @abc.abstractmethod
    def prepare_encrypt(self) -> None:
        pass 
    @abc.abstractmethod
    def post_encrypt(self) -> None:
        pass
    @abc.abstractmethod
    def prepate_decrypt(self) -> None:
        pass
    @abc.abstractmethod
    def verify(self) -> bool:
        pass


class RSA_OAEP(Encrypter):
    def __init__(self, file_path: str):
        self.original_file_path = file_path 

    def prepare_encrypt(self) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        with open(self.original_file_path, 'rb') as file:
            self.file_content = file.read()

    
    def encrypt(self) -> None:
        self.encrypted_content = self.public_key.encrypt(
            self.file_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def post_encrypt(self) -> None:
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)
        
    def prepate_decrypt(self) -> None:
        return None

    def decrypt(self) -> None:
        self.decrypted_content = self.private_key.decrypt(
            self.encrypted_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content
    
class Aes_ecb(Encrypter):
    def __init__(self, file_path: str):
        self.original_file_path = file_path 
    
    def prepare_encrypt(self) -> None:
        key = os.urandom(32)
        counter = 0
        algorithm = algorithms.AES(key)
        self.cipher = Cipher(algorithm, mode = modes.ECB())
        self.encryptor = self.cipher.encryptor()

        with open(self.original_file_path, 'rb') as file:
            self.file_content = file.read()
        
    def encrypt(self) -> None:
        self.encrypted_content = self.encryptor.update(self.file_content)

    def post_encrypt(self) -> None:
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)

    def prepate_decrypt(self) -> None:
        self.decryptor = self.cipher.decryptor()

    def decrypt(self) -> None:
        self.decrypted_content = self.decryptor.update(self.encrypted_content)                    
    
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content
    
class Chacha20(Encrypter):
    def __init__(self, file_path: str):
        self.original_file_path = file_path 
    
    def prepare_encrypt(self) -> None:
        nonce = os.urandom(8)
        key = os.urandom(32)
        counter = 0
        full_nonce = struct.pack("<Q",counter) + nonce
        algorithm = algorithms.ChaCha20(key,full_nonce)
        self.cipher = Cipher(algorithm, mode=None)
        self.encryptor = self.cipher.encryptor()

        with open(self.original_file_path, 'rb') as file:
            self.file_content = file.read()
        
    def encrypt(self) -> None:
        self.encrypted_content = self.encryptor.update(self.file_content)

    def post_encrypt(self) -> None:
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)

    def prepate_decrypt(self) -> None:
        self.decryptor = self.cipher.decryptor()

    def decrypt(self) -> None:
        self.decrypted_content = self.decryptor.update(self.encrypted_content)                    
    
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content
