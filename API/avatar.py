from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/avatar", tags=["avatar"])

class AvatarData(BaseModel):
    idUser: int
    avatar: str

def connexion(mode):
    if mode == 'create':
        user = os.getenv("DB_USER_WRITE")
        password = os.getenv("DB_PASSWORD_WRITE")
    elif mode == 'read':
        user = os.getenv("DB_USER_READ")
        password = os.getenv("DB_PASSWORD_READ")

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)), 
        database=os.getenv("DB_NAME"),
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor
    )





@router.post('/newAvatar')
def new_avatar(data: AvatarData):
    conn = None
    try:
        conn = connexion('create')
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO avatar (avatar, idUser) VALUES (%s, %s)',
                (data.avatar, data.idUser)
            )
        conn.commit()
        return {"message": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: 
            conn.close()
    

@router.get('/getAvatar') 
def get_avatar(idUser: int = Query(..., description="L'ID de l'utilisateur")):
    conn = None
    try:
        conn = connexion('read')
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT avatar FROM avatar WHERE idUser = %s',
                [idUser]
            )
            avatar = cursor.fetchone()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar introuvable")
            
        return avatar
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
  

@router.put('/setAvatar') 
def set_avatar(data: AvatarData):
    conn = None
    try:
        conn = connexion('create')
        with conn.cursor() as cursor:
            cursor.execute(
                'UPDATE avatar SET avatar = %s WHERE idUser = %s',
                (data.avatar, data.idUser)
            )
        conn.commit()
        return {"message": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()