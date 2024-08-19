# Importamos BaseModel de pydantic para definir el esquema de datos
from pydantic import BaseModel, Field

# Importamos Optional de typing para definir campos opcionales
from typing import Optional

# Definimos la clase UserSchema que hereda de BaseModel
class UserSchema(BaseModel):
    # Campo opcional id de tipo int, por defecto es None
    id: Optional[str] = Field(None, description="ID of the user")
    # Campo obligatorio name de tipo str
    name: str
    # Campo obligatorio lastname de tipo str
    lastname: str
    # Campo obligatorio age de tipo int
    age: int
    # Campo obligatorio email de tipo str
    email: str

# Esquema para la creación de usuarios (excluye el campo id)
class UserCreateSchema(BaseModel):
    name: str
    lastname: str
    age: int
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "lastname": "Doe",
                "age": 30,
                "email": "john.doe@example.com"
            }
        }

# Esquema para la actualización de usuarios (excluye el campo id)
class UserUpdateSchema(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    age: Optional[int]
    email: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "lastname": "Doe",
                "age": 30,
                "email": "john.doe@example.com"
            }
        }


