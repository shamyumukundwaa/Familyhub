from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, users, chores, requests, rewards, calendar


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FamilyHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chores.router)
app.include_router(requests.router)
app.include_router(rewards.router)
app.include_router(calendar.router)


@app.get("/")
def root():
    return {"message": "FamilyHub API is running ✅"}
