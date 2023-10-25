from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import os

class Encrypter(ABC):
    @abstractmethod
    def encrypt(self) -> None:
        pass
    @abstractmethod
    def decrypt(self) -> None:
        pass
    @abstractmethod
    def prepare_encrypt(self) -> None:
        pass 
    @abstractmethod
    def post_encrypt(self) -> None:
        pass
    @abstractmethod
    def prepate_decrypt(self) -> None:
        pass
    @abstractmethod
    def verify(self) -> None:
        pass


class RSAEncrypter(Encrypter):
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

    def verify(self):
        return self.file_content == self.decrypted_content
