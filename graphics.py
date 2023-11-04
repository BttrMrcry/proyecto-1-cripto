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

def graphic_type(name,avg_data,mode):
    avg_data = dict(sorted([a for a in avg_data.items()]))
    algorithm = list(avg_data.keys())
    time = list(avg_data.values())
    plt.plot(algorithm, time,marker='o')
    plt.xlabel('Test size in KB')
    plt.ylabel('Time in nanoseconds')
    plt.title(f'{name} as {mode}')
    plt.show()

def bar_graphic(name,avg_data):
    name = str(name)
    algorithm = list(avg_data.keys())
    time = list(avg_data.values())
    plt.bar(algorithm, time)
    plt.xlabel('Test size in KB')
    plt.ylabel('Time in nanoseconds')
    plt.title(f'{name.upper()}')
    plt.show()

def make_graphics(algorithms,test_files,mode,mode_inv):
    avg_data_en = {}
    avg_data_de = {}
    decryption_time = []
    encryption_time = []
    test_1024 = {}
    test_1024_inv = {}
    for algorit in algorithms:
        for test in test_files:
            test:str = test.split(".")[0]
            encryption_time, decryption_time = read_file(algorit.__name__,test)
            test = test.replace('KB','')
            test_int = int(test)
            if test_int == 1024:
                test_1024[algorit.__name__] = avg(encryption_time)
                test_1024_inv[algorit.__name__] = avg(decryption_time)
            avg_data_en[test_int] = avg(encryption_time)
            avg_data_de[test_int] = avg(decryption_time)
        graphic_type(algorit.__name__,avg_data_en,mode)
        graphic_type(algorit.__name__,avg_data_de,mode_inv)
        avg_data_en = {}
        avg_data_de = {}
    bar_graphic(mode,test_1024)
    bar_graphic(mode_inv,test_1024_inv)
    

def graphics():

    CONFIG_FILE_PATH = 'settings.json'
    config = {}
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
    TEST_FOLDER_PATH = config[CONFIG_DATA.TEST_FOLDER_PATH.value]
    test_files = os.listdir(TEST_FOLDER_PATH)
    
    make_graphics(encrypters.Encrypter.__subclasses__(),test_files, "encrypter", "decrypter")
    make_graphics(hashers.Hasher.__subclasses__(),test_files, "hash", "verification")
    make_graphics(signers.Signer.__subclasses__(),test_files, "signed" ,"verification")
            
if __name__ == '__main__':
    graphics()