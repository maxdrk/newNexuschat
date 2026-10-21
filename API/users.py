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

class userId(BaseModel):
    id : int

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class selectUser(BaseModel):
    nom : str

class demande (BaseModel):
    idFrom : int
    idTo : int
    
class updateStatusDemande(BaseModel):
    status: Literal['accepted', 'refused']
    idConv: int

@router.post('/createUser')
def createUser(user: UserCreate):  
    try:
        conn = connexion('create')
        with conn.cursor() as cursor:  
            cursor.callproc('createUser', [user.username, user.email, user.password])  
            cursor.execute('SELECT U.idUser FROM users U JOIN mail M ON M.idMail = U.idMail WHERE M.mail = %s', [user.email])
            created = cursor.fetchone()
            conn.commit() 
        conn.close()
        return {"message": "Utilisateur créé", "idUser": created["idUser"]}
    except pymysql.err.IntegrityError as e:
        if 'email' in str(e).lower() or 'mail' in str(e).lower():
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        elif 'username' in str(e).lower():
            raise HTTPException(status_code=400, detail="Username déjà utilisé")
        else:
            raise HTTPException(status_code=400, detail="Email ou username déjà utilisé")
    


@router.post('/getUser')
def getUser(data: userId):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('CALL getUser(%s)', [data.id])
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
            print(result)
            return {"success" : True,"idUser" : result['idUser']}
    except HTTPException:
        raise   

    except pymysql.err.IntegrityError:
            raise HTTPException(status_code=400)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
            
@router.post('/selectUser')
def selectUser(user : selectUser):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('call selectUser(%s)', [user.nom])
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
    

@router.post('/createDemande')
def createDemande(user : demande):
    try:
        conn = connexion("create")
        with conn.cursor() as cursor:
            cursor.execute('call createDemande(%s,%s)', [user.idFrom, user.idTo])
        conn.commit()
        conn.close()
        return {"message": "ok", "idTo": user.idTo}
    except HTTPException:
        raise
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/getDemandes')
def getDemandes(user : userId):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT D.idDemande, D.fromUser AS idFrom, D.toUser AS idTo,
                       P1.username AS expediteur, P2.username AS destinataire,
                       D.statusD AS status
                FROM demandes D
                JOIN pseudo P1 ON P1.idUser = D.fromUser
                JOIN pseudo P2 ON P2.idUser = D.toUser
                WHERE D.fromUser = %s OR D.toUser = %s
                ORDER BY D.createdAt DESC
            ''', [user.id, user.id])
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
            cursor.execute('SELECT fromUser, toUser FROM demandes WHERE idDemande = %s', [user.idConv])
            demande = cursor.fetchone()
            if not demande:
                raise HTTPException(status_code=404, detail="Demande introuvable")
            cursor.execute('UPDATE demandes SET statusD = %s WHERE idDemande = %s', [user.status, user.idConv])
            if user.status == 'accepted':
                id1, id2 = sorted((demande['fromUser'], demande['toUser']))
                cursor.execute('INSERT IGNORE INTO contacts (idUser1, idUser2) VALUES (%s, %s)', [id1, id2])
        conn.commit()
        conn.close()
        return {"message": "ok"}
    except HTTPException:
        raise
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/getContacts')
def getContacts(user: userId):
    try:
        conn = connexion("read")
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT CASE WHEN C.idUser1 = %s THEN C.idUser2 ELSE C.idUser1 END AS idContact,
                       CASE WHEN C.idUser1 = %s THEN P2.username ELSE P1.username END AS contact
                FROM contacts C
                JOIN pseudo P1 ON P1.idUser = C.idUser1
                JOIN pseudo P2 ON P2.idUser = C.idUser2
                WHERE C.idUser1 = %s OR C.idUser2 = %s
            ''', [user.id, user.id, user.id, user.id])
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


    

