import abc
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey 
from cryptography.exceptions import InvalidSignature
from os import path

class Signer(metaclass = abc.ABCMeta):
    def __init__(self, file_path: str):
        self.original_file_path = file_path
    @abc.abstractmethod
    def sign(self) -> None:
        pass
    @abc.abstractmethod
    def prepare_sign(self) -> None:
        pass 
    @abc.abstractmethod
    def post_sign(self) -> None:
        pass
    @abc.abstractmethod
    def verify(self) -> bool:
        pass

class ECDSA_P521(Signer):
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
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.signed_content)
    
    def verify(self) -> bool:
        try:
            self.public_key.verify(
                signature=self.signed_content,
                data=self.file_content,
                signature_algorithm= ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False



class RSA_PSS(Signer):
    def __init__(self, file_path:str) -> None:
        self.original_file_path = file_path
    
    def prepare_sign(self) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        with open(self.original_file_path, "rb") as file:
            self.file_content = file.read()


    def sign(self) -> None:
        self.signed_content = self.private_key.sign(
            self.file_content,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def post_sign(self) -> None:
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.signed_content)
    
    def verify(self) -> bool:
        try:
            self.public_key.verify(
                self.signed_content,
                self.file_content,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False



class ED_25519(Signer):
    def __init__(self, file_path: str):
        self.original_file_path = file_path
    
    def prepare_sign(self) -> None:
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        with open(self.original_file_path, "rb") as file:
            self.file_content = file.read()

    def sign(self) -> None:
        self.signed_content = self.private_key.sign(
            self.file_content)

    def post_sign(self) -> None:
        return
        result_file_path = f"{path.splitext(self.original_file_path)[0]}.bin"
        with open(result_file_path, 'wb') as file:
            file.write(self.signed_content)
    
    def verify(self) -> bool:
        try:
            self.public_key.verify(
                signature=self.signed_content,
                data=self.file_content)
            return True
        except InvalidSignature:
            return False
