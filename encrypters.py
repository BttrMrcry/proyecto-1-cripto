import abc, os, struct, textwrap
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as primitives_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Encrypter(metaclass = abc.ABCMeta):
    def __init__(self, file_path: str):
        self.original_file_path = file_path 

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
    def prepare_encrypt(self) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        
        with open(self.original_file_path, 'rb') as file:
            readed_content = file.read() 
        self.divided_original_bytes = [readed_content[x:x+190] for x in range(0, len(readed_content), 190)]
        self.divided_encrypted_bytes:list[bytes] = []
        self.divided_decrypted_bytes:list[bytes] = []
        self.file_content = readed_content

    
    def encrypt(self) -> None:
        for block in self.divided_original_bytes:
            encrypted_block = self.public_key.encrypt(
                block,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            self.divided_encrypted_bytes.append(encrypted_block)
    
    def post_encrypt(self) -> None:
        return None
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)
        
    def prepate_decrypt(self) -> None:
        return None

    def decrypt(self) -> None:
        for encrypted_block in self.divided_encrypted_bytes:
            decrypoted_block = self.private_key.decrypt(
            encrypted_block,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
            self.divided_decrypted_bytes.append(decrypoted_block)

    def verify(self) -> bool:
        decrypted_content = bytes()
        for block in self.divided_decrypted_bytes:
            decrypted_content += block
        return self.file_content == decrypted_content
    
class Aes_ecb(Encrypter):
    def prepare_encrypt(self) -> None:
        key = os.urandom(32)
        self.algorithm = algorithms.AES(key)
        self.cipher = Cipher(self.algorithm, mode = modes.ECB())
        self.encryptor = self.cipher.encryptor()
        with open(self.original_file_path, 'rb') as file:
            self.file_content = file.read()
        
    def encrypt(self) -> None:
        padder = primitives_padding.PKCS7(self.algorithm.block_size).padder()
        padded_data = padder.update(self.file_content) + padder.finalize()
        self.encrypted_content = self.encryptor.update(padded_data)

    def post_encrypt(self) -> None:
        return None
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)

    def prepate_decrypt(self) -> None:
        
        self.decryptor = self.cipher.decryptor()


    def decrypt(self) -> None:
        padder = primitives_padding.PKCS7(self.algorithm.block_size).unpadder() 
        padded_data = self.decryptor.update(self.encrypted_content)
        self.decrypted_content = padder.update(padded_data) + padder.finalize()
    
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content
    
class Chacha20(Encrypter):
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
        return None
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)

    def prepate_decrypt(self) -> None:
        self.decryptor = self.cipher.decryptor()

    def decrypt(self) -> None:
        self.decrypted_content = self.decryptor.update(self.encrypted_content)                    
    
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content
    
    

class Aes_gcm(Encrypter):
    def prepare_encrypt(self) -> None:
        key = os.urandom(32)
        counter = 0
        algorithm = algorithms.AES(key)
        nonce = os.urandom(12)
        self.cipher = Cipher(algorithm, mode = modes.GCM(nonce))
        self.encryptor = self.cipher.encryptor()

        with open(self.original_file_path, 'rb') as file:
            self.file_content = file.read()
        
    def encrypt(self) -> None:
        self.encrypted_content = self.encryptor.update(self.file_content)

    def post_encrypt(self) -> None:
        return None
        result_file_path = f"{os.path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.encrypted_content)

    def prepate_decrypt(self) -> None:
        self.decryptor = self.cipher.decryptor()

    def decrypt(self) -> None:
        self.decrypted_content = self.decryptor.update(self.encrypted_content)                    
    
    def verify(self) -> bool:
        return self.file_content == self.decrypted_content

