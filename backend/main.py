# run dev with: uvicorn main:app --reload
# swagger at localhost:8000/docs

from fastapi import FastAPI
from models import PlayerSheet, Template, UserPrompt, PlayerSheetObject
from common import set_env, LOGGER
from templates import UPDATE_JSON, SUGGERISCI_AZIONE_DND_ITA, COSA_SUCCEDE_DOPO_DND_ITA
from chains_utils import init_llm_chain
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse
import json


def read_json(fpath:str):
    with open(fpath, 'r') as file:
        data = json.load(file)
    return data

def write_json(dictionary:dict, fpath:str):
    with open(fpath, 'w') as file:
        json.dump(dictionary, file)


global SHEET_FPATH
global SHEET_FPATH_RESTORE
global CURRENT_PLAYER_SHEET

SHEET_FPATH = "test_player_sheet.json"
SHEET_FPATH_RESTORE = "test_player_sheet_restore.json"
CURRENT_PLAYER_SHEET = read_json(SHEET_FPATH)
# print("***")
# print(CURRENT_PLAYER_SHEET)
write_json(CURRENT_PLAYER_SHEET, SHEET_FPATH_RESTORE)

## fastapi
set_env()

tags_metadata = [
    {"name": "Test", "description": "Metodi per testare OpenAI con dati predefiniti"},
    {"name": "Prod", "description": "Metodi da usare con il resto del mondo"}
]
app = FastAPI(openapi_tags=tags_metadata)

# origins = [
#     "http://localhost:8000",
#     "http://localhost:8001",
#     "http://localhost:8002",

#     "http://0.0.0.0:8000",
#     "http://0.0.0.0:8001",
#     "http://0.0.0.0:8002",
    
#     "http://127.0.0.1:8000",
#     "http://127.0.0.1:8001",
#     "http://127.0.0.1:8002",
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test_sheet", tags=["Test"])
async def test_sheet() -> PlayerSheet:
    return PlayerSheet(**CURRENT_PLAYER_SHEET)


@app.post("/test_with_fake_sheet", tags=["Test"])
async def test_with_fake_sheet(prompt: UserPrompt) -> PlayerSheet:

    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    write_json(CURRENT_PLAYER_SHEET, SHEET_FPATH_RESTORE)

    player_sheet = PlayerSheet(**CURRENT_PLAYER_SHEET)

    update_player_sheet_template = Template(**UPDATE_JSON)

    update_stat_chain = init_llm_chain(prompt_template=update_player_sheet_template.text,
                                       template_variables=update_player_sheet_template.input_variables,
                                       chat_temperature=0.1,
                                       output_key="update_stat_chain_out")

    response = update_stat_chain.run(user_prompt=prompt.prompt,
                                     current_json=player_sheet.json())

    LOGGER.info(f"Risposta raw di OpenAI: {response}")

    try:
        res_dict = eval(response.strip())
        res = PlayerSheet(**res_dict)

        CURRENT_PLAYER_SHEET = res_dict
        write_json(CURRENT_PLAYER_SHEET, SHEET_FPATH)

        LOGGER.info(f"Risposta formattata correttamente: {res}")

    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")

    return res


@app.post("/test_with_fake_sheet_variables_only", tags=["Test"])
async def test_with_fake_sheet_variables_only(prompt: UserPrompt) -> PlayerSheet:
    
    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    write_json(CURRENT_PLAYER_SHEET, SHEET_FPATH_RESTORE)

    player_sheet = PlayerSheet(**CURRENT_PLAYER_SHEET)
    # to optimize openai call
    
    sheet_needed_for_prompt = {
        "ispirazione" : player_sheet.ispirazione,
        "punti_ferita": player_sheet.punti_ferita,
        "punti_ferita_massimi": player_sheet.punti_ferita_massimi,
        "punti_ferita_temporanei": player_sheet.punti_ferita_temporanei,
        "monete_oro": player_sheet.monete_oro,
        "monete_argento": player_sheet.monete_argento,
        "monete_rame": player_sheet.monete_rame,
        "oggetti": [ model.dict() for model in player_sheet.oggetti]
    }

    update_player_sheet_template = Template(**UPDATE_JSON)

    update_stat_chain = init_llm_chain(prompt_template=update_player_sheet_template.text,
                                       template_variables=update_player_sheet_template.input_variables,
                                       chat_temperature=0.1,
                                       output_key="update_stat_chain_out")

    # response = update_stat_chain.run(user_prompt=prompt.prompt,
    #                                  current_json=player_sheet.json())
    response = update_stat_chain.run(user_prompt=prompt.prompt,
                                     current_json=sheet_needed_for_prompt)
    
    
    LOGGER.info(f"Risposta raw di OpenAI: {response}")

    try:
        res_dict = eval(response.strip())
        # res = PlayerSheet(**res_dict)
        player_sheet.ispirazione = res_dict['ispirazione']
        player_sheet.punti_ferita = res_dict['punti_ferita']
        player_sheet.punti_ferita_massimi = res_dict['punti_ferita_massimi']
        player_sheet.punti_ferita_temporanei = res_dict['punti_ferita_temporanei']
        player_sheet.monete_oro = res_dict['monete_oro']
        player_sheet.monete_argento = res_dict['monete_argento']
        player_sheet.monete_rame = res_dict['monete_rame']
        player_sheet.oggetti = [PlayerSheetObject(**oggetto) for oggetto in  res_dict['oggetti']]

        CURRENT_PLAYER_SHEET = player_sheet.dict()
        write_json(CURRENT_PLAYER_SHEET, SHEET_FPATH)

        LOGGER.info(f"Risposta formattata correttamente: {player_sheet}")

    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")

    return player_sheet

@app.post("/test_suggest_action", tags=["Test"])
async def test_suggest_action(prompt: UserPrompt) -> str:
    
    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    player_sheet = PlayerSheet(**CURRENT_PLAYER_SHEET)

    suggest_action_template = Template(**SUGGERISCI_AZIONE_DND_ITA)

    suggest_action_chain = init_llm_chain(prompt_template=suggest_action_template.text,
                                          template_variables=suggest_action_template.input_variables,
                                          chat_temperature=0.7,
                                          output_key="suggest_action_chain_out")

    response = suggest_action_chain.run(user_prompt=prompt.prompt,
                                        player_sheet_json=player_sheet.json())

    LOGGER.info(f"Risposta raw di OpenAI: {response}")

    return response.replace("\"", "").strip()


@app.post("/test_what_happens_later", tags=["Test"])
async def test_what_happens_later(prompt: UserPrompt) -> str:
    
    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    player_sheet = PlayerSheet(**CURRENT_PLAYER_SHEET)
    
    

    suggest_action_template = Template(**COSA_SUCCEDE_DOPO_DND_ITA)

    suggest_action_chain = init_llm_chain(prompt_template=suggest_action_template.text,
                                          template_variables=suggest_action_template.input_variables,
                                          chat_temperature=0.7,
                                          output_key="suggest_action_chain_out")

    response = suggest_action_chain.run(user_prompt=prompt.prompt,
                                        player_sheet_json=player_sheet.json())

    LOGGER.info(f"Risposta raw di OpenAI: {response}")

    return response.replace("\"", "").strip()


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

@app.get("/test_restore/", tags=["Test"])
def test_save() -> PlayerSheet:

    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    CURRENT_PLAYER_SHEET = read_json(SHEET_FPATH_RESTORE)
    
    return PlayerSheet(**CURRENT_PLAYER_SHEET)
    
@app.get("/test_download/", tags=["Test"])
def test_download() -> PlayerSheet:

    global CURRENT_PLAYER_SHEET
    global SHEET_FPATH_RESTORE
    global SHEET_FPATH

    
    
    return FileResponse(SHEET_FPATH_RESTORE, media_type='application/json',filename='player_sheet_test.json')