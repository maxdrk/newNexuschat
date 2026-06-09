from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])

def connexion(mode):
    if mode == 'create':
        user = os.getenv("DB_USER_WRITE")
        password = os.getenv("DB_PASSWORD_WRITE")
    elif mode == 'read':
        user = os.getenv("DB_USER_READ")
        password = os.getenv("DB_PASSWORD_READ")
    else:
        print('mode non existant')    

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor
    )

class Demande (BaseModel):
    userFrom : int
    userTo:int
    status : str

@app.post('/createDemande')
def createDemande(demande : Demande):
    pass