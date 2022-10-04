# intro-distribuidos-TP1

Trabajo práctico de la materia Introducción a los Sistemas Distribuidos

### Prerquisitos

* [Python 3.6](https://www.python.org/downloads/release/python-360/)
* [Pip](https://pip.pypa.io/en/stable/installing/)

### Instalación de librerías

(Aclaración) A partir de este punto, los siguientes comandos deben ejecutarse en la carpeta raíz del proyecto.

Para instalar las librerías requeridas, ejecutar:

```bash
$ pip install -r requirements.txt
```

### Iniciación del servidor

Para iniciar el servidor, se debe ejecutar el siguiente comando:

```bash
$ python3 start-server.py [opciones]
```

Las opciones se enumeran utilizando el comando help:

```bash
$ python3 start-server.py --help | -h
```

### Iniciación del cliente (subida de archivos)

Para realizar la subida de un archivo, se debe ejecutar el siguiente comando, asumiendo que el servidor ya está funcionando:

```bash
$ python3 upload.py [opciones]
```

Las opciones se enumeran utilizando el comando help:

```bash
$ python3 upload.py --help | -h
```

### Iniciación del cliente (descarga de archivos)

Para realizar la descarga de un archivo, se debe ejecutar el siguiente comando, asumiendo que el servidor ya está funcionando:

```bash
$ python3 download.py [opciones]
```

Las opciones se enumeran utilizando el comando help:

```bash
$ python3 download.py --help | -h
```
