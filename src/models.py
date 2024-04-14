from pydantic import BaseModel


class FromAttributes:
    "Permite que los modelos se inicialicen con los atributos que se le pasen al constructor."

    class Config:
        from_attributes = True
