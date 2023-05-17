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
