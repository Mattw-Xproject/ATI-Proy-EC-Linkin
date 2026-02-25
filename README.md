# ATI Proy EC Linkin

Este proyecto es una aplicación Django configurada para ejecutarse en un entorno de contenedores Docker, simulando una arquitectura real con separación de servicios (Apache, Aplicación Web y Base de Datos).

## Arquitectura de Contenedores

El proyecto se divide en 3 contenedores:

1.  **Apache (`linkin_apache`)**: Actúa como proxy inverso, recibiendo las peticiones en el puerto 80 y redirigiéndolas al contenedor web.
2.  **Web (`linkin_web`)**: Contiene la lógica de la aplicación Django y se comunica con la base de datos.
3.  **DB (`linkin_db`)**: Un contenedor ligero (Alpine) que gestiona el volumen `bd_data`, donde se almacena el archivo SQLite (`db.sqlite3`).

## Requisitos Previos

- [Docker](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.

## Instalación y Uso

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clonar el repositorio** (si no lo has hecho ya):
    ```bash
    git clone <url-del-repositorio>
    cd ATI-Proy-EC-Linkin
    ```

2.  **Construir e iniciar los contenedores**:
    Ejecuta el siguiente comando en la raíz del proyecto:
    ```bash
    docker-compose up -d --build
    ```
    Este comando descargará las imágenes necesarias, construirá el contenedor web y levantará los 3 servicios en segundo plano.

3.  **Verificar el estado**:
    Puedes ver si los contenedores están corriendo correctamente con:
    ```bash
    docker-compose ps
    ```

4.  **Acceder a la aplicación**:
    Abre tu navegador y entra en:
    [http://localhost](http://localhost)

## Notas Adicionales

- **Migraciones**: El contenedor web está configurado para ejecutar automáticamente `python manage.py migrate` al iniciar.
- **Persistencia**: La base de datos se guarda en un volumen de Docker llamado `bd_data`. Esto significa que tus datos no se borrarán aunque detengas y elimines los contenedores.
- **Logs**: Para ver lo que está pasando en los contenedores, usa:
  ```bash
  docker-compose logs -f
  ```
