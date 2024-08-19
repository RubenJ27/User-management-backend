# Importamos el módulo psycopg2 para manejar la conexión a la base de datos PostgreSQL
import psycopg2
# Importamos load_dotenv para cargar las variables de entorno desde el archivo .env
from dotenv import load_dotenv
# Importamos os para acceder a las variables de entorno
import os

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# Importamos el esquema de usuario desde el módulo schema.user_schema
from schema.user__schema import UserSchema, UserUpdateSchema

# Definimos la clase UserConnection para manejar la conexión y operaciones con la base de datos
class UserConnection:
    # Atributo de clase para la conexión a la base de datos
    conn = None

    # Método constructor de la clase
    def __init__(self):
        try:
            # Obtenemos las variables de entorno
            dbname = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            host = os.getenv("DB_HOST")
            password = os.getenv("DB_PASSWORD")
            port = os.getenv("DB_PORT")
            
            # Intentamos establecer una conexión a la base de datos PostgreSQL
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                host=host,
                password=password,
                port=port
            )
        except psycopg2.OperationalError as err:
            # Si ocurre un error de conexión, lo imprimimos y cerramos la conexión
            print("Error: Connection to the database failed")
            print(err)
            self.conn.close()

    # Método para escribir datos de usuario en la base de datos
    def write(self, user_data: UserSchema):
        # Usamos un cursor para ejecutar comandos SQL
        with self.conn.cursor() as cur:
            # Ejecutamos una consulta SQL para insertar datos en la tabla "users"
            cur.execute("""
                        INSERT INTO "users"(name, lastname, age, email) VALUES(%(name)s, %(lastname)s, %(age)s, %(email)s) 
                        """, {
                'name': user_data['name'],
                'lastname': user_data['lastname'],
                'age': user_data['age'],
                'email': user_data['email']
            })
            # Confirmamos (commit) la transacción
            self.conn.commit()

    # Método para leer todos los datos de usuario en la base de datos
    def read_all(self):
        if self.conn is None:
            raise Exception("No database connection")
        # Usamos un cursor para ejecutar comandos SQL
        with self.conn.cursor() as cur:
            # Ejecutamos una consulta SQL para buscar todos los datos en la tabla "users"
            cur.execute("""
                        SELECT * FROM "users"
                        """)
            data = cur.fetchall()
            return data
        
    # Método para leer un dato de usuario en la base de datos por ID
    def read_one(self, id):
        if self.conn is None:
            raise Exception("No database connection")
        # Usamos un cursor para ejecutar comandos SQL
        with self.conn.cursor() as cur:
            # Ejecutamos una consulta SQL para buscar todos los datos en la tabla "users"
            cur.execute("""
                        SELECT * FROM "users" WHERE id = %s
                        """, (id,))
            data = cur.fetchone()
            return data

    # Metodo para borra un dato de usuario en la base de datos por ID
    def delete(self, id: str) -> bool:
        if self.conn is None:
            raise Exception("No database connection")
        # Usamos un cursor para ejecutar comandos SQL
        with self.conn.cursor() as cur:
            # Ejecutamos una consulta SQL para buscar todos los datos en la tabla "users"
            cur.execute("""
                        DELETE FROM "users" WHERE id = %s
                        """, (id,))
            self.conn.commit()
            # Verificamos si alguna fila fue afectada
            return cur.rowcount > 0

            
    # Método para actualizar un dato de usuario en la base de datos por ID
    def update(self, user_data: UserUpdateSchema):
        if self.conn is None:
            raise Exception("No database connection")
        # Usamos un cursor para ejecutar comandos SQL
        with self.conn.cursor() as cur:
            # Ejecutamos una consulta SQL para buscar todos los datos en la tabla "users"
            query = """
                UPDATE "users" SET name = %(name)s, lastname = %(lastname)s, age = %(age)s, email = %(email)s WHERE id = %(id)s
            """
            cur.execute(query, user_data)
            self.conn.commit()
            # Verificamos si alguna fila fue afectada
            return cur.rowcount > 0


    # Método destructor de la clase
    def __del__(self):
        # Cerramos la conexión a la base de datos cuando el objeto es destruido
        self.conn.close()