import abc
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes #para sha 2 y sha 3
import cryptography.exceptions
from os import urandom, path

class Hasher(metaclass = abc.ABCMeta):
    def __init__(self, file_path: str):
        self.original_file_path = file_path
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
    def prepare_verify(self) -> None:
        pass
    @abc.abstractmethod
    def verify(self) -> bool:
        pass

class sha2 (Hasher):#heredo de la clase Hashes todos sus métodos
    def prepare_hash(self) -> None:
        self.digest = hashes.Hash(hashes.SHA512())#crea el objeto que va a crear los hashes (es un atributo del objeto sha2)

        with open(self.original_file_path, 'rb') as f:
            self.data = f.read() # Lee el contenido del archivo y lo guarda en "data"
    
    def hash(self) -> None:
        self.digest.update(self.data)#Se genera el hash

    def post_hash(self) -> None:
        self.hash_result = self.digest.finalize()#Regresa el hash objenido. Regresa los bytes
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"  #se guarda el resultado del hash en el archivo con extension .bin
        with open(result_file_path, 'wb') as file:
            file.write(self.hash_result)
    
    def prepare_verify(self) -> None:
        self.verification_digest = hashes.Hash(hashes.SHA512())
    
    def verify(self) -> bool:
        self.verification_digest.update(self.data)
        hash_resultante = self.verification_digest.finalize()
        return hash_resultante == self.hash_result

class sha3 (Hasher):#heredo de la clase Hashes todos sus métodos 
    def prepare_hash(self) -> None:
        self.digest = hashes.Hash(hashes.SHA3_512())#crea el objeto que va a crear los hashes (es un atributo del objeto sha3)

        with open(self.original_file_path, 'rb') as f:
            self.data = f.read() # Lee el contenido del archivo y lo guarda en "data"
    
    def hash(self) -> None:
        self.digest.update(self.data)#Se genera el hash

    def post_hash(self) -> None:
        self.hash_result = self.digest.finalize()#Regresa el hash objenido. Regresa los bytes
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"  #se guarda el resultado del hash en el archivo con extension .bin
        with open(result_file_path, 'wb') as file:
            file.write(self.hash_result)
    
    def prepare_verify(self) -> None:
        self.verification_digest = hashes.Hash(hashes.SHA3_512())
    
    def verify(self) -> bool:
        self.verification_digest.update(self.data)
        hash_resultante = self.verification_digest.finalize()
        return hash_resultante == self.hash_result

class ScryptAlgorithm(Hasher):

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
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.key)
    
    def prepare_verify(self) -> None:
        self.kdf = Scrypt(
            salt=self.salt,
            length=4,
            n=2**14,
            r=8,
            p=1
        )

    def verify(self) -> bool:
        try:
            self.kdf.verify(self.file_content, self.key)
            return True
        except(cryptography.exceptions.InvalidKey, cryptography.exceptions.AlreadyFinalized):
            return False
