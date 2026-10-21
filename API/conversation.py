from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/conversations", tags=["conversations"])


def connexion(mode):
    if mode == 'create':
        user = os.getenv("DB_USER_WRITE")
        password = os.getenv("DB_PASSWORD_WRITE")
    elif mode == 'read':
        user = os.getenv("DB_USER_READ")
        password = os.getenv("DB_PASSWORD_READ")

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor
    )


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[int, list[WebSocket]] = {}

    async def connect(self, conv_id: int, websocket: WebSocket):
        await websocket.accept()
        if conv_id not in self.rooms:
            self.rooms[conv_id] = []
        self.rooms[conv_id].append(websocket)

    def disconnect(self, conv_id: int, websocket: WebSocket):
        if conv_id in self.rooms:
            self.rooms[conv_id].remove(websocket)
            if not self.rooms[conv_id]:
                del self.rooms[conv_id]

    async def broadcast(self, conv_id: int, message: dict):
        if conv_id in self.rooms:
            for ws in self.rooms[conv_id]:
                await ws.send_json(message)


manager = ConnectionManager()


def table_columns(cursor, table_name):
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    return {row['Field'] for row in cursor.fetchall()}


class ConvCreate(BaseModel):
    idUser1: int
    idUser2: int


@router.post('/create')
def create_conversation(data: ConvCreate):
    if data.idUser1 <= 0 or data.idUser2 <= 0:
        raise HTTPException(status_code=400, detail="Les identifiants des utilisateurs doivent être positifs")
    if data.idUser1 == data.idUser2:
        raise HTTPException(status_code=400, detail="Une conversation nécessite deux utilisateurs différents")

    user1, user2 = sorted((data.idUser1, data.idUser2))
    read_conn = None
    write_conn = None
    try:
        # La vérification utilise le compte lecture : le compte d'écriture
        # peut être volontairement limité aux INSERT/UPDATE.
        read_conn = connexion('read')
        with read_conn.cursor() as cursor:
            conversation_columns = table_columns(cursor, 'conversations')
            if {'idUser1', 'idUser2'} <= conversation_columns:
                cursor.execute('''
                    SELECT convId FROM conversations
                    WHERE idUser1 = %s AND idUser2 = %s
                ''', [user1, user2])
            elif {'fromUser', 'toUser'} <= conversation_columns:
                cursor.execute('''
                    SELECT convId FROM conversations
                    WHERE (fromUser = %s AND toUser = %s)
                       OR (fromUser = %s AND toUser = %s)
                ''', [user1, user2, user2, user1])
            else:
                raise HTTPException(status_code=500, detail="Schéma de la table conversations non reconnu")
            legacy_conversations = 'fromUser' in conversation_columns
            existing = cursor.fetchone()
        read_conn.close()
        read_conn = None
        if existing:
            return {"convId": existing['convId']}

        write_conn = connexion('create')
        with write_conn.cursor() as cursor:
            if legacy_conversations:
                cursor.execute(
                    'INSERT INTO conversations (fromUser, toUser) VALUES (%s, %s)',
                    [user1, user2]
                )
            else:
                cursor.execute(
                    'INSERT INTO conversations (idUser1, idUser2) VALUES (%s, %s)',
                    [user1, user2]
                )
            write_conn.commit()
            return {"convId": cursor.lastrowid}
    except pymysql.err.IntegrityError as e:
        if e.args and e.args[0] == 1062:
            # Une autre requête a pu créer la même paire entre le SELECT et l'INSERT.
            retry_conn = connexion('read')
            try:
                with retry_conn.cursor() as cursor:
                    conversation_columns = table_columns(cursor, 'conversations')
                    if {'idUser1', 'idUser2'} <= conversation_columns:
                        cursor.execute('SELECT convId FROM conversations WHERE idUser1 = %s AND idUser2 = %s', [user1, user2])
                    else:
                        cursor.execute('''
                            SELECT convId FROM conversations
                            WHERE (fromUser = %s AND toUser = %s)
                               OR (fromUser = %s AND toUser = %s)
                        ''', [user1, user2, user2, user1])
                    existing = cursor.fetchone()
                if existing:
                    return {"convId": existing['convId']}
            finally:
                retry_conn.close()
        raise HTTPException(status_code=400, detail=f"Impossible de créer la conversation : {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la conversation : {e}")
    finally:
        if read_conn:
            read_conn.close()
        if write_conn:
            write_conn.close()


@router.get('/history/{conv_id}')
def get_history(conv_id: int):
    conn = None
    try:
        conn = connexion('read')
        with conn.cursor() as cursor:
            conversation_columns = table_columns(cursor, 'conversations')
            if {'idUser1', 'idUser2'} <= conversation_columns:
                cursor.execute('SELECT idUser1 AS user1, idUser2 AS user2 FROM conversations WHERE convId = %s', [conv_id])
            else:
                cursor.execute('SELECT fromUser AS user1, toUser AS user2 FROM conversations WHERE convId = %s', [conv_id])
            conv = cursor.fetchone()
            if not conv:
                raise HTTPException(status_code=404, detail="Conversation introuvable")

            message_columns = table_columns(cursor, 'message')
            if 'convId' in message_columns:
                cursor.execute('''
                    SELECT M.messageId, P.username AS auteur, M.contenu,
                           DATE_FORMAT(M.createdAt, '%%H:%%i') AS heure
                    FROM message M
                    JOIN pseudo P ON M.fromUser = P.idUser
                    WHERE M.convId = %s
                    ORDER BY M.createdAt ASC
                ''', [conv_id])
            else:
                cursor.execute('''
                    SELECT M.messageId, P.username AS auteur, M.contenu,
                           DATE_FORMAT(M.createdAt, '%%H:%%i') AS heure
                    FROM message M
                    JOIN pseudo P ON M.fromUser = P.idUser
                    WHERE (M.fromUser = %s AND M.toUser = %s)
                       OR (M.fromUser = %s AND M.toUser = %s)
                    ORDER BY M.createdAt ASC
                ''', [conv['user1'], conv['user2'], conv['user2'], conv['user1']])
            return cursor.fetchall()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.websocket('/ws/{conv_id}/{id_user}/{username}')
async def websocket_endpoint(websocket: WebSocket, conv_id: int, id_user: int, username: str):
    conn = None
    try:
        conn = connexion('read')
        with conn.cursor() as cursor:
            conversation_columns = table_columns(cursor, 'conversations')
            if {'idUser1', 'idUser2'} <= conversation_columns:
                cursor.execute('SELECT idUser1 AS user1, idUser2 AS user2 FROM conversations WHERE convId = %s', [conv_id])
            else:
                cursor.execute('SELECT fromUser AS user1, toUser AS user2 FROM conversations WHERE convId = %s', [conv_id])
            conv = cursor.fetchone()
            message_columns = table_columns(cursor, 'message')
            legacy_messages = 'convId' not in message_columns
        conn.close()
        conn = None
        if not conv or id_user not in (conv['user1'], conv['user2']):
            await websocket.close(code=1008)
            return

        to_user = conv['user2'] if id_user == conv['user1'] else conv['user1']
        await manager.connect(conv_id, websocket)
        while True:
            data = await websocket.receive_json()
            conn = connexion('create')
            with conn.cursor() as cursor:
                if legacy_messages:
                    cursor.execute('INSERT INTO message (contenu, fromUser, toUser) VALUES (%s, %s, %s)', [data['contenu'], id_user, to_user])
                else:
                    cursor.execute('INSERT INTO message (convId, contenu, fromUser) VALUES (%s, %s, %s)', [conv_id, data['contenu'], id_user])
                conn.commit()
            conn.close()
            conn = None

            await manager.broadcast(conv_id, {
                'auteur': username,
                'contenu': data['contenu'],
                'heure': data.get('heure', ''),
                'idUser': id_user
            })
    except WebSocketDisconnect:
        manager.disconnect(conv_id, websocket)
    finally:
        if conn:
            conn.close()
