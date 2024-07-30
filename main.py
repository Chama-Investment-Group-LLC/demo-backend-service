"""
Initializes the FastAPI application and defines the root route.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from notifications.endpoints import router as notification_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(notification_router)


@app.get("/ping")
async def root():
    """
    Root route that returns a simple message.
    """
    return "PONG!"
