# Proyecto 1 de criptografía
Este proyecto tiene el objetivo de comparar el tiempo de ejecución de algunos de los principales algoritmos criptográficos. El proyecto está escrito en Python y se utiliza los algoritmos de la biblioteca [Cryptography](https://cryptography.io/en/latest/).


# Requisitos
En la lista siguiente se muestran los requisitos necesarios para correr la prueba rápida del programa.

- **Conexión a internet**
- **Docker Engine**. Las instrucciones de instalación se pueden encontrar [aquí](https://docs.docker.com/get-docker/).
- **Git**. Click [aquí](https://git-scm.com/downloads) para ver las instrucciones de instalación.
- **Linux o macOS** (Windows también funciona si se corren manualmente los comandos de Docker)

El programa ha sido probado en Ubuntu 20.04 y macOS Sonoma. También funciona en Windows 10 y Windows 11, pero la ejecución de los comandos de Docker se debe hacer manualmente.

# Verificación de requisitos

## Docker
Para verificar que Docker esta instalado correctamente se debe correr el siguiente comando.

    docker run hello-world

La salida de este comando debe ser como la siguiente.

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

Si la salida no es la esperada se debe verificar la instalación de Docker.

## Git
Para verificar la instalación de git simplemente se debe ejecutar

    git --version

La salida debe ser similar a la siguiente.

    git version 2.34.1

## Interprete de comando
En Linux y macOS Bash debería estar instalado por defecto. Para verificarlo ejecute el comando siguiente.

    Bash --version 

Si se muestra correctamente la versión del interprete podrá correr el archivo `run.sh` usado más adelante. Si no esta instalado podrá correr los comandos de Docker manualmente.

# Ejecución del programa

## Obtención del código fuente
Primero se debe clonar el repositorio. Esto lo puede realizar con el comando siguiente.

    git clone https://github.com/BttrMrcry/proyecto-1-cripto.git

El resto de los comando los ejecutaremos en el directorio del repositorio, asi que nos moveremos a él con el comando siguiente.

    cd proyecto1-crypto

## Configuración opcional
El proyecto esta configurado por defecto para realizar 100 iteraciones por algoritmo utilizando multi-procesamiento. Esta configuración es solo con fines demostrativos. Los datos reales se generaron con 200 iteraciones con multi-procesamiento deshabilitado. Esta configuración se puede modificar en `settings.json`.

```json
{
    "testFolderPath": "test-files",
    "numberOfIterations": 100,
    "enableMultiprocessing": true,
    "resultsFolderPath": "results",
    "desableEncryptionAlgorithm": [
    ]
}
```
**NO MODIFICAR** `testFolderPath` **NI** `resultsFolderPath`. 

La ejecución ejecución de alguno de los algoritmos se puede deshabilitar agregándolo a `desableEncryptionAlgorithm`.

## Demostración rápida

Para ejecutar una demostración rápida del código se necesita cumplir con el requisito de tener instalado **Bash**. De no ser así por favor ir a la demostración manual en la siguiente sección.

La demostración rápida se realiza ejecutando el comando siguiente.

    ./run.sh

Puede ser que necesite agregar permisos de ejecución al archivo. Si recibe el mensaje `bash: ./run.sh: Permission denied` por favor ejecute el comando siguiente y repita el paso anterior.

    chmod +x run.sh

Cuando el comando se ejecute comenzará la construcción automática de la imagen del contenedor necesario para ejecutar el código, se realizaran los cronometrajes a los algoritmos, se generaran gráficas representando estos datos y al final se eliminara automáticamente el contenedor.

Al terminar la ejecución se generarán dos carpetas:
1. **plots/**: Contendrá las gráficas representando los datos obtenidos.
2. **results/**: Se podrán encontrar en formato CSV los resultados en bruto de las pruebas para cada algoritmo y cada vector de prueba. 

## Demostración manual

En caso de no poder ejecutar `run.sh` se pueden ejecutar los comandos contenidos en este script manualmente. Los comando son los siguientes:

```
docker build -t crypto .
docker run -t -d --name runner crypto
docker exec runner python runners.py
docker exec runner python graphics.py
docker cp runner:/crypto-runner/results ./results
docker cp runner:/crypto-runner/plots ./plots
docker stop runner
docker rm runner
docker image rm crypto
```

### Creación de la imagen del contenedor
El comando siguiente ejecuta el dockerfile para construir la imagen requerida. A la imagen se nombra crypto.

    docker build -t crypto .

### Creación del contenedor 
Este comando crea un nuevo contenedor llamado runner a partir de la imagen cryto.
    
    docker run -t -d --name runner crypto

### Ejecución de los cronometrajes
Con este comando se crean los datos.

    docker exec runner python runners.py

### Creación de las gráficas
Aquí se llama al script que crea las gráficas.
    
    docker exec runner python graphics.py

### Extracción de datos de contenedor
Estos comandos copian los datos generados dentro del contenedor al sistema de archivos de host para poder ser vistos.

    docker cp runner:/crypto-runner/results ./results
    docker cp runner:/crypto-runner/plots ./plots

### Limpieza
El primer comando detiene el contenedor. El segundo elimina al contenedor y el último elimina la imagen del contenedor.

    docker stop runner
    docker rm runner
    docker image rm crypto