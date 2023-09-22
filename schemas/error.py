from pydantic import BaseModel
from typing import Optional, List

from model.opiniao import Opiniao

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de erro será representada
    """
    mesage: str