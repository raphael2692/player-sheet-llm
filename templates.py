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
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
=======
>>>>>>> 950a24488f45867e9c92f128a26ede2f4060a29b

SUGGERISCI_AZIONE_DND_ITA = {
    "text" : """
Il tuo compito è suggerire la prossima azione che deve compiere un certo personaggio in una campagna di Dungeons and Dragons basandoti sul prompt utente. 
<<<<<<< HEAD
Devi essere originale e mai banale.
Devi proporre azioni con un breve o brevissimo orizzonte temporale.
Le tue proposte devono corrispondere ad azioni fattibili con le regole di Dungens And Dragons 5E. Fai riferimento il più possibile al manuale giocatore.
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Ti viene chiesto: {user_prompt}
Rispondi (max 150 parole):
=======
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Ti viene chiesto: {user_prompt}
Rispondi (max 100 parole):
>>>>>>> 950a24488f45867e9c92f128a26ede2f4060a29b
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}


COSA_SUCCEDE_DOPO_DND_ITA = {
    "text" : """
Il tuo compito è descrivere cosa succederà nella campagna di Dungeons and Dragons di un dato personaggio a seguito di quanto descritto nel prompt utente. 
<<<<<<< HEAD
Devi essere originale e mai banale.
Devi proporre azioni con un breve o brevissimo orizzonte temporale.
Le tue proposte devono corrispondere ad azioni fattibili con le regole di Dungens And Dragons 5E. Fai riferimento il più possibile al manuale giocatore.
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Cosa succede: {user_prompt}
Rispondi (max 150 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}
>>>>>>> Stashed changes
=======
Tutto quello che sai su questo personaggio è scritto in questo JSON: {player_sheet_json}
Cosa succede: {user_prompt}
Rispondi (max 100 parole):
""",
    "input_variables" : ['player_sheet_json', 'user_prompt']
}
>>>>>>> 950a24488f45867e9c92f128a26ede2f4060a29b
