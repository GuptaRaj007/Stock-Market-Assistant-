from pymongo import MongoClient
from urllib.parse import quote_plus
import streamlit as st 
# Raw credentials
db_user_raw = st.secrets["MONGO_USER"]
db_password_raw = st.secrets["MONGO_PASS"]


# URL encoding
db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

# MongoDB URI
uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.xx3zem0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_mongo_collection():
    """Connects to MongoDB Atlas and returns the stock collection."""
    client = MongoClient(uri)
    db = client["stock_db"]
    return db["stock_col"]

