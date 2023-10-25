from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom, path
from time import perf_counter

class Hashes(ABC):
    @abstractmethod
    def hash(self) -> None:
        pass
    @abstractmethod
    def prepare_hash(self) -> None:
        pass 
    @abstractmethod
    def post_hash(self) -> None:
        pass
    @abstractmethod
    def verify(self) -> None:
        pass

class Scrypt_Algorith(Hashes):
    def __init__(self, file_path: str):
        self.original_file_path = file_path
    
    def prepare_hash(self) -> None:
        self.salt = urandom(128)
        self.kdf = Scrypt(
            salt=self.salt,
            length=4,
            n=2**14,
            r=8,
            p=1
        )
        with open(self.original_file_path, "rb") as file:
            self.file_content = file.read()

    def hash(self) -> None:
        self.key = self.kdf.derive(key_material=self.file_content)

    def post_hash(self) -> None:
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.key)

    def verify(self) -> None:
        try:
            self.kdf.verify(self.file_content, self.key)
            print("Hash llevado a cabo de manera satisfactoria")
        except:
            print("El hash no coincide, posible elemento modificado")
