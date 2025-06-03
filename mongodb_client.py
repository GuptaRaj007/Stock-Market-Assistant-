from pymongo import MongoClient
from urllib.parse import quote_plus
import streamlit as st

# Secure credentials from Streamlit secrets
db_user_raw = st.secrets["MONGO_DB_USER"]
db_password_raw = st.secrets["MONGO_DB_PASSWORD"]

# URL encoding
db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

# ✅ Updated URI with explicit TLS support
uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.xx3zem0.mongodb.net/?tls=true&retryWrites=true&w=majority"

def get_mongo_collection():
    """Connects to MongoDB Atlas and returns the stock collection."""
    client = MongoClient(uri)
    db = client["stock_db"]
    return db["stock_col"], db["fo_col"]
