from pydantic import BaseModel, Field, validator

class PlayerSheet(BaseModel):
    ispirazione: int
    punti_ferita: int
    punti_ferita_massimi: int
    punti_ferita_temporanei: int
    monete_oro: int
    monete_argento: int
    monete_rame: int
    oggetti: list

class Template(BaseModel):
    text: str
    input_variables: list