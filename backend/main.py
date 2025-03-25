# main.py
from fastapi import FastAPI
from routes.email_routes import router as email_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(email_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


# ✅ Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
