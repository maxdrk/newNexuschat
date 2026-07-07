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


class ConvCreate(BaseModel):
    idUser1: int
    idUser2: int


@router.post('/create')
def create_conversation(data: ConvCreate):
    try:
        conn = connexion('create')
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT convId FROM conversations
                WHERE (fromUser = %s AND toUser = %s)
                OR (fromUser = %s AND toUser = %s)
            ''', [data.idUser1, data.idUser2, data.idUser2, data.idUser1])
            existing = cursor.fetchone()
            if existing:
                return {"convId": existing['convId']}
            cursor.execute(
                'INSERT INTO conversations (fromUser, toUser) VALUES (%s, %s)',
                [data.idUser1, data.idUser2]
            )
            conn.commit()
            return {"convId": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.get('/history/{conv_id}')
def get_history(conv_id: int):
    try:
        conn = connexion('read')
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT fromUser, toUser FROM conversations WHERE convId = %s',
                [conv_id]
            )
            conv = cursor.fetchone()
            if not conv:
                raise HTTPException(status_code=404, detail="Conversation introuvable")

            cursor.execute('''
                SELECT M.messageId, P.username AS auteur, M.contenu,
                       DATE_FORMAT(M.createdAt, '%%H:%%i') AS heure
                FROM message M
                JOIN pseudo P ON M.fromUser = P.idUser
                WHERE (M.fromUser = %s AND M.toUser = %s)
                   OR (M.fromUser = %s AND M.toUser = %s)
                ORDER BY M.createdAt ASC
            ''', [conv['fromUser'], conv['toUser'],
                  conv['toUser'], conv['fromUser']])
            return cursor.fetchall()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.websocket('/ws/{conv_id}/{id_user}/{username}')
async def websocket_endpoint(websocket: WebSocket, conv_id: int, id_user: int, username: str):
    await manager.connect(conv_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            conn = connexion('create')
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO message (contenu, fromUser, toUser) VALUES (%s, %s, %s)',
                    [data['contenu'], id_user, data['toUser']]
                )
                conn.commit()
            conn.close()

            await manager.broadcast(conv_id, {
                'auteur': username,
                'contenu': data['contenu'],
                'heure': data.get('heure', ''),
                'idUser': id_user
            })
    except WebSocketDisconnect:
        manager.disconnect(conv_id, websocket)
