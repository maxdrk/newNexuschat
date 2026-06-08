from fastapi import FastAPI
from users import router as user_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="NexusChat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, tags=["users"])

@app.get("/")
def root():
    return {"message": "Les APIS Nexuschat sont entrain de tournées :)"}