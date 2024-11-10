# Proyecto de Gestión de Usuarios

Este proyecto es una aplicación para la gestión de usuarios utilizando Python y PostgreSQL. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos de usuarios.

## Estructura del Proyecto

├── **pycache**/
├── .env
├── .gitignore
├── config/
│ ├── **init**.py
├── main.py
├── models/
│ ├── **init**.py
│ ├── user_connection.py
├── requeriments.txt
├── schema/
│ ├── **init**.py
│ ├── user\_\_schema.py
├── venv/
│ ├── Include/
│ ├── Lib/
│ ├── Scripts/

## Instalación

1. Clona el repositorio:

   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. Crea y activa un entorno virtual:

   ```sh
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   .\venv\Scripts\activate # En windows
   source venv/bin/activate      # En Unix o macOS
   ```

3. Instala las dependencias:

   ```sh
   pip install -r requeriments.txt
   ```

4. Crea un archivo [`.env`]" en la raíz del proyecto con las siguientes variables de entorno:
   ```env
   DB_NAME=<nombre_de_la_base_de_datos>
   DB_USER=<usuario_de_la_base_de_datos>
   DB_HOST=<host_de_la_base_de_datos>
   DB_PASSWORD=<contraseña_de_la_base_de_datos>
   DB_PORT=<puerto_de_la_base_de_datos>
   ```

## Uso

1. Ejecuta la aplicación:

   ```sh
   python main.py
   ```

   ```
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. La aplicación se conectará a la base de datos PostgreSQL utilizando las variables de entorno definidas en el archivo [`.env`]
3. Accede a la documentación de Swagger en tu navegador web en: `http://127.0.0.1:8000/docs`

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está licenciado bajo mi Licencia. Consulta el archivo `LICENSE` para más detalles.
