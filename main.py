# run dev with: uvicorn main:app --reload
# swagger at localhost:8000/docs

from fastapi import FastAPI
from models import PlayerSheet, Template
from common import set_env, LOGGER
from templates import UPDATE_JSON
from chains_utils import init_llm_chain


set_env()

tags_metadata = [
    {"name": "Test", "description": "Metodi per testare OpenAI con dati predefiniti"},
    {"name": "Prod", "description": "Metodi da usare con il resto del mondo"}
]
app = FastAPI(openapi_tags=tags_metadata)


@app.post("/test_with_fake_sheet", tags=["Test"])
async def test_with_fake_sheet(prompt:str) -> PlayerSheet:
    player_sheet_json = {
        "ispirazione": 3,
        "punti_ferita": 20,
        "punti_ferita_massimi": 27,
        "punti_ferita_temporanei": 0,
        "monete_oro": 1200,
        "monete_argento": 15,
        "monete_rame": 33,
        "oggetti": [
            "stivali elfici",
            "sfera luminosa"
        ]
    }
    
    player_sheet = PlayerSheet(**player_sheet_json)
    
    update_player_sheet_template = Template(**UPDATE_JSON)
    
    
    update_stat_chain = init_llm_chain(prompt_template=update_player_sheet_template.text, 
                                        template_variables=update_player_sheet_template.input_variables, 
                                        chat_temperature=0.1, 
                                        output_key="update_stat_chain_out")
    
    response = update_stat_chain.run(user_prompt=prompt, 
                                        current_json=player_sheet.json())
    
    LOGGER.info(f"Risposta raw di OpenAI: {response}")
    
    try: 
        res_dict = eval(response.strip())
        res = PlayerSheet(**res_dict)
        LOGGER.info(f"Risposta formattata correttamente: {res}")
        
    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")
        
    return res
    

@app.get("/test_with_fake_prompt_and_sheet/", tags=["Test"])
async def test_with_fake_prompt_and_sheet() -> PlayerSheet:
    player_sheet_json = {
        "ispirazione": 3,
        "punti_ferita": 20,
        "punti_ferita_massimi": 27,
        "punti_ferita_temporanei": 0,
        "monete_oro": 1200,
        "monete_argento": 15,
        "monete_rame": 33,
        "oggetti": [
            "stivali elfici",
            "sfera luminosa"
        ]
    }
    
    player_sheet = PlayerSheet(**player_sheet_json)
    
    update_player_sheet_template = Template(**UPDATE_JSON)
    
    user_prompt = "aggiungi una moneta d'oro e un paio di occhiali da sole magici"
    
    update_stat_chain = init_llm_chain(prompt_template=update_player_sheet_template.text, 
                                        template_variables=update_player_sheet_template.input_variables, 
                                        chat_temperature=0.1, 
                                        output_key="update_stat_chain_out")
    
    response = update_stat_chain.run(user_prompt=user_prompt, 
                                        current_json=player_sheet.json())
    
    LOGGER.info(f"Risposta raw di OpenAI: {response}")
    
    try: 
        res_dict = eval(response.strip())
        res = PlayerSheet(**res_dict)
        LOGGER.info(f"Risposta formattata correttamente: {res}")

    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")

    return res