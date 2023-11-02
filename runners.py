import hashers, signers, encrypters, time, gc, json, os
from typing import Type
from dataclasses import dataclass
from enum import Enum
from tqdm import tqdm



CONFIG_FILE_PATH = 'settings.json'

class CONFIG_DATA(Enum):
    TEST_FOLDER_PATH = 'testFolderPath'
    NUM_ITERATIONS = 'numberOfIterations'
    DESABLE_ENCRYPTION_ALGORITHM = 'desableEncryptionAlgorithm'

@dataclass
class Result: 
    encryption_time:int
    verification_time:int
    verified:bool

def benchmark_encrypter(encrypter: encrypters.Encrypter) -> Result:
    gc.disable()
    encrypter.prepare_encrypt()
    encryption_start = time.perf_counter_ns()
    encrypter.encrypt()
    encryption_end = time.perf_counter_ns()
    encryption_time = encryption_end - encryption_start
    encrypter.post_encrypt()
    encrypter.prepate_decrypt()
    decryption_start = time.perf_counter_ns()
    encrypter.decrypt()
    decryption_end = time.perf_counter_ns()
    decryption_time = decryption_end -decryption_start
    verification = encrypter.verify()
    gc.enable()
    results = Result(
        encryption_time = encryption_time,
        verification_time = decryption_time,
        verified = verification
    )
    return results

def benchmark_hasher(hasher: hashers.Hasher) -> Result:
    gc.disable()
    hasher.prepare_hash()
    hash_start = time.perf_counter_ns()
    hasher.hash()
    hash_end = time.perf_counter_ns()
    hashing_time = hash_end - hash_start
    hasher.post_hash()
    hasher.prepare_verify()
    hash_start = time.perf_counter_ns()
    verification = hasher.verify()
    hash_end = time.perf_counter_ns()
    verification_time = hash_end -hash_start
    gc.enable()
    results = Result(
        encryption_time = hashing_time,
        verification_time= verification_time,
        verified = verification
    )
    return results

def benchmark_signer(signer: signers.Signer) -> Result:
    gc.disable()
    signer.prepare_sign()
    hash_start = time.perf_counter_ns()
    signer.sign()
    hash_end = time.perf_counter_ns()
    signing = hash_end - hash_start
    signer.post_sign()
    hash_start = time.perf_counter_ns()
    verification = signer.verify()
    hash_end = time.perf_counter_ns()
    verification_time = hash_end - hash_start
    gc.enable()
    results = Result(
        encryption_time = signing,
        verification_time= verification_time,
        verified = verification
    )
    return results
    



def run_algorithms():
    #Reads configuration file
    config = {}
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
    NUM_ITERATIONS = config[CONFIG_DATA.NUM_ITERATIONS.value]
    TEST_FOLDER_PATH = config[CONFIG_DATA.TEST_FOLDER_PATH.value]
    DESABLED_ALGORITHMS = config[CONFIG_DATA.DESABLE_ENCRYPTION_ALGORITHM.value]
    test_file_names = os.listdir(TEST_FOLDER_PATH)
    test_files = [os.path.join(TEST_FOLDER_PATH, name) for name in test_file_names]

    print('========Encryption algorithms section========')
    for Encrypter in encrypters.Encrypter.__subclasses__():
        if Encrypter.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Encrypter.__name__}')
            continue
        print(f'testing: {Encrypter.__name__}')
        for test in tqdm(test_files):
            for iteration in tqdm(range(NUM_ITERATIONS)):
                working_Encrypter = Encrypter(test)
                test_result = benchmark_encrypter(working_Encrypter)
                if not test_result.verified:
                    print('Something is wrong')

    print('========Hashing algorithms section========')
    for Hasher in hashers.Hasher.__subclasses__():
        if Hasher.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Hasher.__name__}')
            continue
        print(f'testing: {Hasher.__name__}')
        for test in tqdm(test_files):
            for iteration in tqdm(range(NUM_ITERATIONS)):
                working_hasher = Hasher(test)
                test_result = benchmark_hasher(working_hasher)
                if not test_result.verified:
                    print('Something is wrong')

    print('========Signing algorithms section========')
    for Signer in signers.Signer.__subclasses__():
        if Signer.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Signer.__name__}')
            continue
        print(f'testing: {Signer.__name__}')
        for test in tqdm(test_files):
            for iteration in tqdm(range(NUM_ITERATIONS)):
                working_singer = Signer(test)
                test_result = benchmark_signer(working_singer)
                if not test_result.verified:
                    print('Something is wrong')


if __name__ == '__main__':
    run_algorithms()




