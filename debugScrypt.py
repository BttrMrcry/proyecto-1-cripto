import hashers, os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import cryptography.exceptions

debugScrypt = hashers.ScryptAlgorithm("poquito-texto.txt")

debugScrypt.prepare_hash()
debugScrypt.hash()
print(debugScrypt.key)
debugScrypt.prepare_verify()
print(debugScrypt.verify())
