from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, users, chores, requests, rewards, calendar


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FamilyHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local browser file paths (file:///) to connect
    allow_credentials=False,  # Must be set to False when allowing all origins via "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chores.router)
app.include_router(requests.router)
app.include_router(rewards.router)
app.include_router(calendar.router)


@app.get("/")
def root():
    return {"message": "FamilyHub API is running ✅"}
