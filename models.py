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
    
class PlayerCombatActions(BaseModel):
    nome: str
    descrizione: str
    
class PlayerBonusActions(BaseModel):
    nome: str
    descrizione: str

class PlayerReactions(BaseModel):
    nome: str
    descrizione: str

class PlayerRacialTraits(BaseModel):
    nome: str
    descrizione: str
    
class PlayerClassFeatures(BaseModel):
    nome: str
    descrizione: str
    
class PlayerFeats(BaseModel):
    nome: str
    descrizione: str

     
class PlayerSheet(BaseModel):
    nome_personaggio: str
    avatar: str
    motto: str
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
    
    tratti_razziali: List[PlayerRacialTraits]
    azioni_combattimento: List[PlayerCombatActions]
    privilegi_classe: List[PlayerClassFeatures]
    talenti: List[PlayerFeats]
    reazioni: List[PlayerReactions]
    azioni_bonus: List[PlayerBonusActions]
    
    oggetti: List[PlayerSheetObject]
    
class Template(BaseModel):
    text: str
    input_variables: list
    
class UserPrompt(BaseModel):
    prompt : str