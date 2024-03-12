from mongoengine import connect
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use environment variables for MongoDB connection details
MONGODB_URL = os.getenv('MONGODB_URL', "")
DB_NAME = os.getenv('DB_NAME', "")

def db_connect():
    """Connect to MongoDB."""
    connect(db=DB_NAME, host=MONGODB_URL, alias="default")

# Call db_connect at the start of your application to establish the database connection
db_connect()
