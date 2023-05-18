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
Tieni in considerazione le regole dalla 5a edizione di Dungeons and Dragons.
Il tuo compito è suggerire la prossima azione che deve compiere un certo personaggio in una campagna di Dungeons and Dragons basandoti sul prompt utente. 
Devi essere originale e mai banale.
Devi proporre azioni con un breve o brevissimo orizzonte temporale.
Le tue proposte devono corrispondere esattamente ad azioni fattibili con le regole di Dungens And Dragons 5E. Fai riferimento il più possibile al manuale giocatore.
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Ti viene chiesto: {user_prompt}
Rispondi (max 150 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}


COSA_SUCCEDE_DOPO_DND_ITA = {
    "text" : """
Tieni in considerazione le regole dalla 5a edizione di Dungeons and Dragons.
Il tuo compito è descrivere cosa succederà nella campagna di Dungeons and Dragons di un dato personaggio a seguito di quanto descritto nel prompt utente. 
Devi essere originale e mai banale.
Devi proporre azioni con un breve o brevissimo orizzonte temporale.
Le tue proposte devono corrispondere esattamente ad azioni fattibili con le regole di Dungens And Dragons 5E. Fai riferimento il più possibile al manuale giocatore.
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Cosa succede: {user_prompt}
Rispondi (max 150 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}
