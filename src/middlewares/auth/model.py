from pydantic import BaseModel
from enum import Enum
from pydantic import model_validator
from models import FromAttributes


class Endpoint(BaseModel):
    method: str
    path: str
