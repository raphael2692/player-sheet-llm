UPDATE_JSON = {
    "text" : """
Aggiorna il JSON sottostante in base al prompt dell'utente. 
Rispondi con solo e soltanto il JSON aggiornato, non aggiungere altro.

current_json: {current_json}
prompt: {user_prompt}
updated_json:
""",
    "input_variables" : ['current_json', 'user_prompt']
}

SUGGERISCI_AZIONE_DND_ITA = {
    "text" : """
Il tuo compito è suggerire la prossima azione che deve compiere un certo personaggio in una campagna di Dungeons and Dragons basandoti sul prompt utente. 
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Ti viene chiesto: {user_prompt}
Rispondi (max 100 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}


COSA_SUCCEDE_DOPO_DND_ITA = {
    "text" : """
Il tuo compito è descrivere cosa succederà nella campagna di Dungeons and Dragons di un dato personaggio a seguito di quanto descritto nel prompt utente. 
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Cosa succede: {user_prompt}
Rispondi (max 100 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}
