# pip3 install -r requirements.txt
pip install pip --upgrade
pip install loguru
pip install openai
pip install fastapi["all"]
pip install httpx
pip install langchain
pip freeze 
uvicorn main:app --host 0.0.0.0 --port 8000 --reload