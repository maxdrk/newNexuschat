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

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post('/createUser')
def createUser(user: UserCreate):  
    try:
        conn = connexion('create')
        with conn.cursor() as cursor:  
            cursor.callproc('createUser', [user.username, user.email, user.password])  
            conn.commit() 
        conn.close()
        return {"message": "Utilisateur créé"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="Email ou username déjà utilisé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/getUser')
def getUser(id: int):
    try:
        conn = connexion("read")  
        with conn.cursor() as cursor:
            cursor.execute('CALL getUser(%s)', [id])  
            result = cursor.fetchone()  
        conn.close()
        return result
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="Aucune donnée trouvée")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/login')
def login(user : UserLogin):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('call loginUser(%s,%s)', [user.email, user.password])
            result = cursor.fetchone()
        conn.close()
        if  not result:
            return False
        else:
            return True
    except HTTPException:
        raise   

    except pymysql.err.IntegrityError:
            raise HTTPException(status_code=400)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
            

    

