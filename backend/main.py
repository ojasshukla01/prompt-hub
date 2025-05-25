from fastapi import FastAPI
from routers import prompts, users
from database import Base, engine

app = FastAPI()

# Include routers
app.include_router(prompts.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to PromptHub Backend API!"}
