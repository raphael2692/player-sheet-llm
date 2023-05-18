# run dev with: uvicorn main:app --reload
# swagger at localhost:8000/docs

from fastapi import FastAPI
from models import PlayerSheet, Template, UserPrompt
from common import set_env, LOGGER
from templates import UPDATE_JSON, SUGGERISCI_AZIONE_DND_ITA, COSA_SUCCEDE_DOPO_DND_ITA
from chains_utils import init_llm_chain
from fastapi.middleware.cors import CORSMiddleware

set_env()

tags_metadata = [
    {"name": "Test", "description": "Metodi per testare OpenAI con dati predefiniti"},
    {"name": "Prod", "description": "Metodi da usare con il resto del mondo"}
]
app = FastAPI(openapi_tags=tags_metadata)

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# test data
test_player_sheet_json = {
    "nome_personaggio": "Sam Sottofrasca",
    "classe": "Ladro",
    "avatar": "https://cdn.mage.space/generate/e05fef03d4b54c4cab7445900e712743.png",
    "livello": 5,
    "razza": "Mezzuomo",
    "motto": "Cavalier con quattro palle, il nemico ti è alle spalle",
    "allineamento": "Caotico Neutrale",
    "ispirazione": 3,
    "ca": 14,
    "punti_ferita": 20,
    "punti_ferita_massimi": 27,
    "punti_ferita_temporanei": 0,
    "monete_oro": 1200,
    "monete_argento": 15,
    "monete_rame": 33,
    "statistiche": [
        {"nome": "Forza", "valore": 8, "modificatore": -1},
        {"nome": "Destrezza", "valore": 17, "modificatore": 3},
        {"nome": "Costituzione", "valore": 12, "modificatore": 1},
        {"nome": "Intelligenza", "valore": 14, "modificatore": 2},
        {"nome": "Saggezza", "valore": 10, "modificatore": 0},
        {"nome": "Carisma", "valore": 14, "modificatore": 2},
    ],
    "competenze": [
        {"nome": "Nascondersi", "bonus": 9},
        {"nome": "Investigare", "bonus": 8},
        {"nome": "Acrobazia", "bonus": 6},
        {"nome": "Rapidità di mano", "bonus": 6},
    ],
    "oggetti": [
        {"nome": "Stivali elfici", "descrizione": "Ottieni vantaggio nelle prove di Furtività",
            "utilizzi": "illimitati"},
        {"nome": "Sfera luminosa", "descrizione": "Gravita intorno al personaggio illuminando l'area",
            "utilizzi": "illimitati"},
        {"nome": "Arco corto +1",
            "descrizione": "1d6 di danno performante a distanza, +1 a colpire e al danno", "utilizzi": "80"},
        {"nome": "Stocco", "descrizione": "1d8 di danno performante in mischia",
            "utilizzi": "illimitato"},
    ],

    "tratti_razziali": [
        {"nome": "Fortunato", "descrizione": "Se rolli 1 su un d20 puoi tirare di nuovo"},
        {"nome": "Coraggioso", "descrizione": "Ottieni vantaggio se spaventato"},
        {"nome": "Leggiadria dei mezzuomini",
            "descrizione": "Puoi muoverti attraverso creature più grande di te"},
        {"nome": "Furtività naturale",
            "descrizione": "Puoi provare a nasconderti dietro una creatura più grande di te"},
    ],
    "azioni_combattimento": [
        {"nome": "Attaccare"},
        {"nome": "Scattare"},
        {"nome": "Disingaggiare"},
        {"nome": "Schivare"},
        {"nome": "Usare un rampino"},
        {"nome": "Nascondersi"},
        {"nome": "Usare un oggetto"},
        {"nome": "Preparare un'azione"},

    ],
    "privilegi_classe": [
        {"nome": "Attacco furtivo",
            "descrizione": "Una volta a turno può attaccare con un arma perforante aggiungendo un 3d6 al danno"},
        {"nome": "Azione scaltra",
            "descrizione": "Può usare un'azione bonus per scattare, disingaggiare o nascondersi"},
        {"nome": "Mani veloci", "descrizione": "Può usare il bonus di azione scaltra per usare un oggetto, fare una prova di Rapidità di mano o rimuovere una trappola"},
    ],
    "talenti": [
        {"nome": "Tiratore scelto", "descrizione": "Quando usa un arco, una volta per turno può rinunciare al bonus di competenza per colpire per aggiungere 10 danni"},
        {"nome": "Esploratore di dungeon", "descrizione": "Ottiene vantaggio nelle prove investigazione per cercare porte nascoste e trappole, e nei tiri salvezza sulle trappole"},
    ],
    "reazioni": [
        {"nome": "Attacco di opportunità", "descrizione": "Può attaccare un nemico che cerca di passare vicino"},
        {"nome": "Schivata prodigiosa", "descrizione": "Può usare una reazione per dimezzare i danni ricevuti"},

    ],
    "azioni_bonus": [
        {"nome": "Azione scaltra"},
        {"nome": "Mani veloci"},
    ],
}


@app.get("/test_sheet", tags=["Test"])
async def test_sheet() -> PlayerSheet:
    return PlayerSheet(**test_player_sheet_json)


@app.post("/test_with_fake_sheet", tags=["Test"])
async def test_with_fake_sheet(prompt: UserPrompt) -> PlayerSheet:

    player_sheet = PlayerSheet(**test_player_sheet_json)

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
        LOGGER.info(f"Risposta formattata correttamente: {res}")

    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")

    return res


@app.post("/test_with_fake_sheet_variables_only", tags=["Test"])
async def test_with_fake_sheet_variables_only(prompt: UserPrompt) -> PlayerSheet:

    player_sheet = PlayerSheet(**test_player_sheet_json)
    # to optimize openai call
    
    sheet_needed_for_prompt = {
        "ispirazione" : player_sheet.ispirazione,
        "punti_ferita": player_sheet.punti_ferita,
        "punti_ferita_massimi": player_sheet.punti_ferita_massimi,
        "punti_ferita_temporanei": player_sheet.punti_ferita_temporanei,
        "monete_oro": player_sheet.monete_oro,
        "monete_argento": player_sheet.monete_argento,
        "monete_rame": player_sheet.monete_rame,
        "oggetti": player_sheet.oggetti
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
        player_sheet.oggetti = res_dict['oggetti']
        
        LOGGER.info(f"Risposta formattata correttamente: {player_sheet}")

    except Exception as e:
        LOGGER.error(f"Impossibile formattare la risposta di OpenAI: {e}")

    return player_sheet

@app.post("/test_suggest_action", tags=["Test"])
async def test_suggest_action(prompt: UserPrompt) -> str:

    player_sheet = PlayerSheet(**test_player_sheet_json)

    suggest_action_template = Template(**SUGGERISCI_AZIONE_DND_ITA)

    suggest_action_chain = init_llm_chain(prompt_template=suggest_action_template.text,
                                          template_variables=suggest_action_template.input_variables,
                                          chat_temperature=0.9,
                                          output_key="suggest_action_chain_out")

    response = suggest_action_chain.run(user_prompt=prompt.prompt,
                                        player_sheet_json=player_sheet.json())

    LOGGER.info(f"Risposta raw di OpenAI: {response}")

    return response.replace("\"", "").strip()


@app.post("/test_what_happens_later", tags=["Test"])
async def test_what_happens_later(prompt: UserPrompt) -> str:

    player_sheet = PlayerSheet(**test_player_sheet_json)
    
    

    suggest_action_template = Template(**COSA_SUCCEDE_DOPO_DND_ITA)

    suggest_action_chain = init_llm_chain(prompt_template=suggest_action_template.text,
                                          template_variables=suggest_action_template.input_variables,
                                          chat_temperature=0.9,
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
