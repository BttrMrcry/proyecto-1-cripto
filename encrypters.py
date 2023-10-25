from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    def encrypt():
        pass
    @abstractmethod
    def decript():
        pass
    @abstractmethod
    def prepare_encript():
        pass 
    @abstractmethod
    def prepate_decript():
        pass