from fastapi import FastAPI
from .dependencies import db_connect
from .routers import user, product, transaction

app = FastAPI()

# Initialize MongoDB connection
db_connect()

# Include routers from the routers module
app.include_router(user.router)
app.include_router(product.router)
app.include_router(transaction.router)
