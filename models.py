from pydantic import BaseModel
from typing import List

class PlayerSheetObject(BaseModel):
    nome: str
    descrizione: str
    utilizzi: str
    
class PlayerStat(BaseModel):
    nome: str
    valore: int
    modificatore: int
    
class PlayerProficiency(BaseModel):
    nome: str
    bonus: int
     
class PlayerSheet(BaseModel):
    nome_personaggio: str
    avatar: str
    classe: str
    razza: str
    livello: int
    allineamento: str
    ispirazione: int
    ca: int
    punti_ferita: int
    punti_ferita_massimi: int
    punti_ferita_temporanei: int
    monete_oro: int
    monete_argento: int
    monete_rame: int
    statistiche: List[PlayerStat]
    competenze: List[PlayerProficiency]
    oggetti: List[PlayerSheetObject]
    
class Template(BaseModel):
    text: str
    input_variables: list
    
class UserPrompt(BaseModel):
    prompt : str