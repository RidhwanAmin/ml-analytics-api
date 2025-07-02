from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.events import router as events_router
from api.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup code here, e.g., database connection
    init_db()  # Assuming this is a function to initialize the database
    yield
    # Teardown code here, e.g., close database connection

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, 
    allow_origins = ['*'],
    allow_credentials = True, 
    allow_methods=["*"], 
    allow_headers = ["*"]

)
app.include_router(events_router, prefix="/api/events")

@app.get("/")
async def root():
    return {"message": "Hello Worlder"}

# health check 
@app.get("/healthz")
def read_api_health(): 
    return {"status": "ok ok je lah "}