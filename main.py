from fastapi import Body, FastAPI, HTTPException, status
import hotels

app = FastAPI()

app.include_router(hotels.router)