import abc
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes #para sha 2 y sha 3
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

class sha2 (Hashes):#heredo de la clase Hashes todos sus métodos
    def __init__(self, file_path: str):#método constructor, recibe un path y lo guarda como un atributo del objeto
        self.original_file_path = file_path
    
    def prepare_hash(self) -> None:
        self.digest = hashes.Hash(hashes.SHA512())#crea el objeto que va a crear los hashes (es un atributo del objeto sha2)

        with open(self.original_file_path, 'rb') as f:
            self.data = f.read() # Lee el contenido del archivo y lo guarda en "data"
    
    def hash(self) -> None:
        self.digest.update(self.data)#Se genera el hash

    def post_hash(self) -> None:
        self.hash_result = self.digest.finalize()#Regresa el hash objenido. Regresa los bytes
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"  #se guarda el resultado del hash en el archivo con extension .bin
        with open(result_file_path, 'wb') as file:
            file.write(self.hash_result)
    
    def verify(self) -> bool:
        hash_calculado = hashes.Hash(hashes.SHA512())
        hash_calculado.update(self.data)
        hash_resultante = hash_calculado.finalize()

        return hash_resultante == self.hash_result

class sha3 (Hashes):#heredo de la clase Hashes todos sus métodos
    def __init__(self, file_path: str):#método constructor, recibe un path y lo guarda como un atributo del objeto
        self.original_file_path = file_path
    
    def prepare_hash(self) -> None:
        self.digest = hashes.Hash(hashes.SHA3_512())#crea el objeto que va a crear los hashes (es un atributo del objeto sha3)

        with open(self.original_file_path, 'rb') as f:
            self.data = f.read() # Lee el contenido del archivo y lo guarda en "data"
    
    def hash(self) -> None:
        self.digest.update(self.data)#Se genera el hash

    def post_hash(self) -> None:
        self.hash_result = self.digest.finalize()#Regresa el hash objenido. Regresa los bytes
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"  #se guarda el resultado del hash en el archivo con extension .bin
        with open(result_file_path, 'wb') as file:
            file.write(self.hash_result)
    
    def verify(self) -> bool:
        hash_calculado = hashes.Hash(hashes.SHA3_512())
        hash_calculado.update(self.data)
        hash_resultante = hash_calculado.finalize()

        return hash_resultante == self.hash_result

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
