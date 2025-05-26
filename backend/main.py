from fastapi import FastAPI
from routers import prompts, users, comments, follows, auth
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)  # <== Include the new /token endpoint!
app.include_router(prompts.router)
app.include_router(users.router)
app.include_router(comments.router)
app.include_router(follows.router)
app.include_router(auth.router)

# Allow frontend requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000","https://nihcevicnytxaxuxnucs.supabase.co"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to PromptHub Backend API!"}
