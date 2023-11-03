import hashers, signers, encrypters, time, gc, json, os, csv
from typing import Type
from dataclasses import dataclass
from enum import Enum
from tqdm import tqdm
import concurrent.futures

CSV_fIELDS = ['Iteration', 'Encryption Time', 'Decryption Time', 'Verification']

CONFIG_FILE_PATH = 'settings.json'

class CONFIG_DATA(Enum):
    TEST_FOLDER_PATH = 'testFolderPath'
    NUM_ITERATIONS = 'numberOfIterations'
    DESABLE_ENCRYPTION_ALGORITHM = 'desableEncryptionAlgorithm'
    RESULTS_FOLDER_PATH = 'resultsFolderPath'
    ENABLE_MULTIPROCESSING = 'enableMultiprocessing'
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
    RESULTS_FOLDER_PATH = config[CONFIG_DATA.RESULTS_FOLDER_PATH.value]
    ENABLE_MULTIPROCESSING = config[CONFIG_DATA.ENABLE_MULTIPROCESSING.value]
    try:
        os.mkdir(RESULTS_FOLDER_PATH)
    except:
        print('Folder already exist')
    test_file_names = os.listdir(TEST_FOLDER_PATH)
    test_files = [os.path.join(TEST_FOLDER_PATH, name) for name in test_file_names]
    cores = 1
    if ENABLE_MULTIPROCESSING:
        cores = os.cpu_count()
        if cores:
            cores = max(cores, 1)

    print('========Encryption algorithms section========')
    for Encrypter in encrypters.Encrypter.__subclasses__():
        if Encrypter.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Encrypter.__name__}')
            continue
        print(f'testing: {Encrypter.__name__}')
        for test in test_files:
            test_file_name = os.path.basename(test)
            csv_filename = os.path.join(RESULTS_FOLDER_PATH, f'{Encrypter.__name__}_{test_file_name.split(".")[0]}.csv')
            print(f'Test vector: {test_file_name}')
            results = []
            with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as Executor:
                encryption_workers = [Encrypter(test) for _ in range(NUM_ITERATIONS)]
                results = list(tqdm(Executor.map(benchmark_encrypter, encryption_workers), total=len(encryption_workers))) 
            with open(csv_filename, 'w+') as csv_file:
                csvwriter = csv.writer(csv_file)
                csvwriter.writerow(CSV_fIELDS)
                for i, r in enumerate(results):
                    csvwriter.writerow([i, r.encryption_time, r.verification_time, r.verified])
                    if not r.verified:
                        print('Something is wrong')


    print('========Hashing algorithms section========')
    for Hasher in hashers.Hasher.__subclasses__():
        if Hasher.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Hasher.__name__}')
            continue
        print(f'testing: {Hasher.__name__}')
        for test in test_files:
            test_file_name = os.path.basename(test)
            csv_filename = os.path.join(RESULTS_FOLDER_PATH, f'{Hasher.__name__}_{test_file_name.split(".")[0]}.csv')
            print(f'Test vector: {os.path.basename(test)}')
            results = []
            with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as Executor:
                hash_workers = [Hasher(test) for _ in range(NUM_ITERATIONS)]
                results = list(tqdm(Executor.map(benchmark_hasher, hash_workers), total=len(hash_workers)))
            with open(csv_filename, 'w+') as csv_file:
                csvwriter = csv.writer(csv_file)
                csvwriter.writerow(CSV_fIELDS)
                for i, r in enumerate(results):
                    csvwriter.writerow([i, r.encryption_time, r.verification_time, r.verified])
                    if not r.verified:
                        print('Something is wrong')

    print('========Signing algorithms section========')
    for Signer in signers.Signer.__subclasses__():
        if Signer.__name__ in DESABLED_ALGORITHMS:
            print(f'Skipping: {Signer.__name__}')
            continue
        print(f'testing: {Signer.__name__}')
        for test in test_files:
            test_file_name = os.path.basename(test)
            csv_filename = os.path.join(RESULTS_FOLDER_PATH, f'{Signer.__name__}_{test_file_name.split(".")[0]}.csv')
            print(f'Test vector: {os.path.basename(test)}')
            results = []
            with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as Executor:
                sign_workers = [Signer(test) for _ in range(NUM_ITERATIONS)]
                results = list(tqdm(Executor.map(benchmark_signer, sign_workers), total=len(sign_workers)))
            with open(csv_filename, 'w+') as csv_file:
                csvwriter = csv.writer(csv_file)
                csvwriter.writerow(CSV_fIELDS)
                for i, r in enumerate(results):
                    csvwriter.writerow([i, r.encryption_time, r.verification_time, r.verified])
                    if not r.verified:
                        print('Something is wrong')



if __name__ == '__main__':
    run_algorithms()




