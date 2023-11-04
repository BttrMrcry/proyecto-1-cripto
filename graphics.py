import hashers, signers, encrypters, os, csv, json
import matplotlib.pylab as plt
from runners import CONFIG_DATA

RESULTS_PATH = "plots"

#Función que realiza el promedio de los tiempos
def avg(rows):
    add = sum(rows)
    return (add/len(rows))/(1000000)

#Función que lee las columnas de los tiempos de cada csv (cifrado y descifrado) y los regresa como arreglos
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

#Ordena los valores de los test y los gráfica en forma de puntos comparando el tamaño del test contra el tiempo que tardo
def graphic_type(name,avg_data,mode):
    avg_data = dict(sorted([a for a in avg_data.items()]))
    algorithm = list(avg_data.keys())
    time = list(avg_data.values())
    plt.plot(algorithm, time,marker='o')
    plt.xlabel('Test size in KB')
    plt.ylabel('Time in miliseconds')
    plt.title(f'{" ".join(name.split("_"))} {mode}'.upper())
    #Guardamos las gráficas de puntos
    plt.savefig(os.path.join(RESULTS_PATH, f'{name}_{mode}.png'))
    
    #Limpia el buffer de las gráficas ()
    plt.clf()

#Compara el tiempo de los algoritmos con el test de 1024 Kbs, comparando cada algoritmo contra el tiempo que tardo
def bar_graphic(name,avg_data,type_Al):
    name = str(name)
    algorithm = list(avg_data.keys())
    time = list(avg_data.values())
    plt.bar(algorithm, time)
    plt.xlabel('Algorithm')
    plt.ylabel('Time in miliseconds')
    plt.title(f'{" ".join(type_Al.split("_"))} {name}'.upper())
    
    #Con esto ponemos el valor en milisegundos en las gráficas de barras
    for algorithm, time in zip(algorithm, time):
        plt.text(algorithm, time, (f'{time: .4f}'), ha='center', va='bottom')
    
    #Guardamos las gráficas de barras
    plt.savefig(os.path.join(RESULTS_PATH, f'{type_Al}_{name}.png'))

    plt.clf()

def make_graphics(algorithms,test_files,mode,mode_inv,type_Al):
    avg_data_en = {}#promedio de encriptación/hash/firma
    avg_data_de = {}#promedio de descifrado/verificación de hash/ verificación de firma
    decryption_time = []#Las columnas de cada archivo csv para tener los tiempos de descifrado/verificaciónhash/verificaciónfirma
    encryption_time = []#Las columnas de cada archivo csv para tener los tiempos de encriptación/hash/firma
    test_1024 = {}#Guarda todos los test de 1024 Kb (1 MB) de cada algoritmo agrupado en su categoría {nombreAlgoritmo:promedioCifrado/hash/firma}
    test_1024_inv = {}#{nombreAlgoritmo : promediodesCifrado/verificacionHash/verificacionFirma}

    #Para cada algoritmo se recorre cada uno de los test (1 Kb, 10 Kb, etc)
    for algorit in algorithms:
        for test in test_files:
            test:str = test.split(".")[0]#Se le quita la concatenación ".txt"
            encryption_time, decryption_time = read_file(algorit.__name__,test)#Se lee cada uno de los archivos csv y retorna 2 arreglos con sus respc. tiempos 
            test = test.replace('KB','')#Se le quita la cadena "KB"
            test_int = int(test)#Lo anterior se castea a int (para usarlo como llave del diccionario)
            if test_int == 1024:#Si el test corresponde a 1024 Kb (1 MB) se guarda en los respectivos diccionarios
                test_1024[algorit.__name__] = avg(encryption_time)#Función que calcula el promedio de todos los tiempos {chacha20 : 2.3, RSA: 3.2, ...}
                test_1024_inv[algorit.__name__] = avg(decryption_time)
            avg_data_en[test_int] = avg(encryption_time)#Función que calcula el promedio de todos los tiempos de un solo algoritmo de todos sus casos {chacha20 1kb : 2.0, chacha20 10 kb: 5.0, ...}
            avg_data_de[test_int] = avg(decryption_time)

        graphic_type(algorit.__name__,avg_data_en,mode)#Genera la gráfica de cada algoritmo (mode = encriptación)
        graphic_type(algorit.__name__,avg_data_de,mode_inv)##Genera la gráfica de cada algoritmo (mode = descifrado)
        avg_data_en = {}#Se borran los datos de un algoritmo en especifico, porque para la siguiente vuelta usaremos otro algoritmo
        avg_data_de = {}

    bar_graphic(mode,test_1024,type_Al)#Genera gráficas de barras de cifrado para comparar entre los distintos algoritmos con el test de 1024 Kbs
    bar_graphic(mode_inv,test_1024_inv,type_Al)#Genera lo mismo pero para descifrado

    if test_1024.get("RSA_OAEP",0):
        test_1024.pop("RSA_OAEP")
        test_1024_inv.pop("RSA_OAEP")
        bar_graphic(mode,test_1024,"Encrypters_without_RSA_OAEP")#Genera gráficas de barras quitando RSA_OAEP, pues su valor es muy grande respecto a los demás y 
        bar_graphic(mode_inv,test_1024_inv,"Encrypters_without_RSA_OAEP")#Provoca que las demas barras se vean muy pequeñas

def graphics():

    CONFIG_FILE_PATH = 'settings.json'#Archivo donde estan las rutas para leer el archivo "test-files" donde estan los test de dif. Kbs
    config = {}
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
    TEST_FOLDER_PATH = config[CONFIG_DATA.TEST_FOLDER_PATH.value]
    test_files = os.listdir(TEST_FOLDER_PATH)#Guardamos el listado del directorio test-files (1KB.txt, etc)
    
    #Creamos la carpeta donde se van a guardar las imagenes de las gráficas de puntos y de barras
    try:
        os.mkdir(RESULTS_PATH)
    except:
        print('Folder already exist')
    
    #Se llama a la función que prepara los datos para hacer las gráficas: se le manda el nombre de cada tipo de encriptador
    # hash y firma. Después se le manda todos los archivos de testeo y al final el nombre de crifrado y verificación
    make_graphics(encrypters.Encrypter.__subclasses__(),test_files, "encryption", "decryption","encrypters")
    make_graphics(hashers.Hasher.__subclasses__(),test_files, "hashing", "verification","hashers")
    make_graphics(signers.Signer.__subclasses__(),test_files, "signing" ,"verification","signers")
            
if __name__ == '__main__':
    graphics()