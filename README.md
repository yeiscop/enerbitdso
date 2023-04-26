```txt
███████╗██████╗     ██████╗ ███████╗ ██████╗ 
██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔═══██╗
█████╗  ██████╔╝    ██║  ██║███████╗██║   ██║
██╔══╝  ██╔══██╗    ██║  ██║╚════██║██║   ██║
███████╗██████╔╝    ██████╔╝███████║╚██████╔╝
╚══════╝╚═════╝     ╚═════╝ ╚══════╝ ╚═════╝ 
                                             
```

# Introducción

Un programa de línea de comandos para preparar y empujar reportes de lectura desde el api de enerBit al MDM.

Se distribuye como un paquete de Python ejecutable.

# Como empezar

## Instalación

1. Crear un ambiente virtual de Python para aislar la instalación del paquete de otros paquetes.

```sh
python3 -m venv venv
source ./venv/bin/activate
```

1. Instalar paquete usando pip (asegurarse de tener activo el ambiente virtual).

```sh
python -m pip install .
```

1. Comprobar la instalación con el comando de ayuda

```sh
enerbitdso --help
```

# Uso

El comando es `enerbitdso`.

Se tiene una ayuda usando la opción `--help`.
Esta explica los sub-comandos y las opciones disponibles de cada uno.

Esta herramienta usa las variables de entorno para configurar su ejecución.

## Sub-comandos

### `prepare`

Preparar los archivos `xml` para una lista de medidores.

Este comando toma un archivo con un serial de medidor por línea.
Para cada uno, consulta los datos
