# Importamos FastAPI y HTTPException de la librería fastapi
from fastapi import FastAPI, HTTPException, logger, Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

# Importamos la clase UserConnection desde el módulo models.user_connection
from models.user_connection import UserConnection

# Importamos el esquema de usuario desde el módulo schema.user_schema
from schema.user__schema import UserCreateSchema, UserSchema, UserUpdateSchema  

# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

# Creamos una instancia de la conexión de usuario
conn = UserConnection()

# Definimos una ruta GET en la raíz ("/")
@app.get("/", status_code=HTTP_200_OK)  
def root():
    try:
        # Intentamos leer todos los datos de la conexión
        data = conn.read_all()
        items = []
        for data in conn.read_all():
            dictionary = {}
            dictionary["id"] = data[0]
            dictionary["name"] = data[1]
            dictionary["lastname"] = data[2]
            dictionary["age"] = data[3]
            dictionary["email"] = data[4]
            items.append(dictionary)
        return items
    except Exception as e:
        # Si ocurre una excepción, la registramos y lanzamos una HTTPException con código 500 y el detalle del error
        logger.error(f"Error al leer los datos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
      #return {"message": "Bienvenido a la API de FastAPI"}


# Definimos una ruta GET en "/api/user/id" para obtener datos de usuario por ID
@app.get("/api/user/{id}", summary="Get User by ID", status_code=HTTP_200_OK)
def get_one(id: str):
    try:
        # Intentamos leer los datos del usuario con el ID proporcionado
        data = conn.read_one(id)

        if not data:
            # Si no se encontro ninguna fila, lanzamos una HTTPException con código 404
            raise HTTPException(status_code=404, detail="User not found")

        # Creamos un diccionario con los datos del usuario encontrado
        user_dictionary = {
            "id": data[0],
            "name": data[1],
            "lastname": data[2],
            "age": data[3],
            "email": data[4]
        }
        
        # Devolvemos el diccionario como respuesta
        return user_dictionary

    except Exception as e:
        # Si ocurre una excepción, lanzamos una HTTPException con código 500 y el detalle del error
        raise HTTPException(status_code=500, detail=str(e))


# Definimos una ruta POST en "/api/insert" para insertar datos de usuario
@app.post("/api/insert" , summary="Insert User", status_code=HTTP_201_CREATED)
def insert(user_data: UserCreateSchema):
    try:
        data = user_data.model_dump()
        # Intentamos escribir los datos del usuario en la conexión
        conn.write(data)
        # Si todo va bien, devolvemos un estado "ok"
        return Response(status_code=HTTP_201_CREATED)
    except Exception as e:
        # Si ocurre una excepción, lanzamos una HTTPException con código 500 y el detalle del error
        raise HTTPException(status_code=500, detail=str(e))


# Definimos la ruta PUT en "/api/update/id" para actualizar datos de usuario por ID
@app.put("/api/update/{id}", summary="Update User by ID", status_code=HTTP_204_NO_CONTENT)
def update(id: str, user_data: UserUpdateSchema):
    try:
        data = user_data.model_dump()
        data["id"] = id
        # Intentamos actualizar los datos del usuario con el ID proporcionado
        if not conn.update(data):
            # Si no se actualizó ninguna fila, lanzamos una HTTPException con código 404
            raise HTTPException(status_code=404, detail="User not found")
        # Si todo va bien, devolvemos un estado "ok"
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        # Si ocurre una excepción, lanzamos una HTTPException con código 500 y el detalle del error
        raise HTTPException(status_code=500, detail=str(e))


# Definimos una ruta DELETE en "/api/delete/id" para eliminar datos de usuario por ID
@app.delete("/api/delete/{id}", summary="Delete User by ID", status_code=HTTP_204_NO_CONTENT)
def delete(id: str):
    try:
         # Intentamos eliminar los datos del usuario con el ID proporcionado
        if not conn.delete(id):
        # Si no se eliminó ninguna fila, lanzamos una HTTPException con código 404
            raise HTTPException(status_code=404, detail="User not found")
        # Si todo va bien, devolvemos un estado "ok"
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        # Si ocurre una excepción, lanzamos una HTTPException con código 500 y el detalle del error
        raise HTTPException(status_code=500, detail=str(e))

