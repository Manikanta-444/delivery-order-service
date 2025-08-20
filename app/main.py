from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routes import customers, addresses, orders, drivers, auth
from app.database.connection import engine, Base
from app.utils.logger import logger

logger.debug("Starting Delivery Order Service at debug level...")

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delivery Order Service",
    description="Microservice for managing delivery orders, customers, and drivers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router, prefix="/api/v1")
app.include_router(addresses.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Delivery Order Service is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "order-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
