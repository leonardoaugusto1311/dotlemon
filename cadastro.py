from pymongo import MongoClient
from urllib.parse import quote_plus


username = "leonardoaugusto199813"
password = quote_plus("August@123")


client = MongoClient(f'mongodb+srv://{username}:{password}@precificacao.axzys.mongodb.net/?retryWrites=true&w=majority&appName=Precificacao')

db = client.precificacao
colecao_login = db['login']


result = colecao_login.insert_many([
    {
        "login": "dotlemon_master",
        "senha": "dotlemon" , 
        "tipo": 1 ,
        "cliente_id" : "2" ,
        "cliente" : "dotlemon"
    },
    {
        "login": "operacional_dotlemon",
        "senha": "opdot" , 
        "tipo": 0 ,
        "cliente_id" : "2"  ,
        "cliente" : "dotlemon"
    }
    #{
    #    "login": "login1",
    #    "senha": "senha1" , 
    #    "tipo": 1 ,
    #    "cliente_id" :  ,
    #    "cliente" : 
    #}
])

print("Documentos inseridos com IDs:", result.inserted_ids)
