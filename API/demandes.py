from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
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

class demande (BaseModel):
    idFrom : int
    idTo : int
    
class updateStatusDemande(BaseModel):
    status: Literal['accepted', 'refused']
    idConv: int
    userFrom : int
    userTo:int
    status : str

class userIdentity(BaseModel):
    userId : int

@router.post('/createDemande')
def createDemande(user : demande):
    try:
        conn = connexion("create")
        with conn.cursor() as cursor:
            cursor.execute('call createDemande(%s,%s)', [user.idFrom, user.idTo])
        conn.commit()
        conn.close()
        return {"message": "ok"}
    except HTTPException:
        raise
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/getDemandes')
def getDemandes(user : userIdentity):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('call getDemandes(%s)', [user.id])
            result = cursor.fetchall()
        conn.close()
        if  not result:
            return False
        else:
            print(result)
            return result
    except HTTPException:
        raise   

    except pymysql.err.IntegrityError:
            raise HTTPException(status_code=400)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/updateStatusDemande')
def updateStatusDemande(user : updateStatusDemande):
    try:
        conn = connexion("create")
        with conn.cursor() as cursor:
            cursor.execute('call updateStatusDemande(%s,%s)', [user.status, user.idConv])
        conn.commit()
        conn.close()
        return {"message": "ok"}
    except HTTPException:
        raise
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    