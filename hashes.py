import abc
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom, path

class Hashes(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def hash(self) -> None:
        pass
    @abc.abstractmethod
    def prepare_hash(self) -> None:
        pass 
    @abc.abstractmethod
    def post_hash(self) -> None:
        pass
    @abc.abstractmethod
    def verify(self) -> bool:
        pass

class ScryptAlgorithm(Hashes):
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

    def verify(self) -> bool:
        try:
            self.kdf.verify(self.file_content, self.key)
            return True
        except:
            return False
