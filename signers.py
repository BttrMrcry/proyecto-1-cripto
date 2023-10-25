from abc import ABC, abstractmethod
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from os import urandom, path
from time import perf_counter

class Signer(ABC):
    @abstractmethod
    def sign(self) -> None:
        pass
    @abstractmethod
    def prepare_sign(self) -> None:
        pass 
    @abstractmethod
    def post_sign(self) -> None:
        pass
    @abstractmethod
    def verify(self) -> None:
        pass

class ECDSA_P521(Signer):
    def __init__(self, file_path: str):
        self.original_file_path = file_path
    
    def prepare_sign(self) -> None:
        self.private_key = ec.generate_private_key(
        ec.SECP521R1()
        )
        self.public_key = self.private_key.public_key()
        with open(self.original_file_path, "rb") as file:
            self.file_content = file.read()

    def sign(self) -> None:
        self.signed_content = self.private_key.sign(
            data=self.file_content, 
            signature_algorithm=ec.ECDSA(hashes.SHA256()))

    def post_sign(self) -> None:
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.signed_content)
    
    def verify(self) -> None:
        try:
            self.public_key.verify(
                signature=self.signed_content,
                data=self.file_content,
                signature_algorithm= ec.ECDSA(hashes.SHA256()))
            print("Firmado confirmado usando ECDSA P521")
        except(ValueError, TypeError):
            print("Firmado de manera incorrecta")
