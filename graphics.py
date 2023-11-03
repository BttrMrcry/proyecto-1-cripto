import hashers, signers, encrypters, os, csv, json
import matplotlib.pylab as plt
from runners import CONFIG_DATA

def avg(rows):
    add = sum(rows)
    return add/len(rows)

def read_file(name,test):
    decryption_time = []
    encryption_time = []
    with open(os.path.join('results', f'{name}_{test}.csv'), 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            encryption_time.append(int(row[1]))
            decryption_time.append(int(row[2]))
        return encryption_time, decryption_time

def graphics():

    CONFIG_FILE_PATH = 'settings.json'
    config = {}
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
    TEST_FOLDER_PATH = config[CONFIG_DATA.TEST_FOLDER_PATH.value]
    test_files = os.listdir(TEST_FOLDER_PATH)

    avg_data_en = {}
    avg_data_de = {}
    decryption_time = []
    encryption_time = []
    for Encrypter in encrypters.Encrypter.__subclasses__():
        for test in test_files:
            test:str = test.split(".")[0]
            encryption_time, decryption_time = read_file(Encrypter.__name__,test)
            test = test.replace('KB','')
            test_int = int(test)
            avg_data_en[test_int] = avg(encryption_time)
            avg_data_de[test_int] = avg(decryption_time)
        avg_data_en = dict(sorted([a for a in avg_data_en.items()]))
        avg_data_de = dict(sorted([a for a in avg_data_de.items()]))
        algorithm = list(avg_data_en.keys())
        time = list(avg_data_en.values())
        plt.scatter(algorithm, time)
        plt.xlabel('Test size in KB')
        plt.ylabel('Time in nanoseconds')
        plt.title(f'{Encrypter.__name__}')
        plt.show()
        avg_data_de = {}
        avg_data_en = {}
            
if __name__ == '__main__':
    graphics()