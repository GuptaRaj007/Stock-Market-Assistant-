from pymongo import MongoClient
from urllib.parse import quote_plus
import streamlit as st

# Secure credentials from Streamlit secrets
db_user_raw = st.secrets["MONGO_DB_USER"]
db_password_raw = st.secrets["MONGO_DB_PASSWORD"]

# URL encoding
db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

# ✅ Robust MongoDB URI for Streamlit Community Cloud
uri = (
    f"mongodb+srv://{db_user}:{db_password}@cluster0.xx3zem0.mongodb.net/"
    f"?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
)

def get_mongo_collection():
    """Connects to MongoDB Atlas and returns the stock and F&O collections."""
    try:
        client = MongoClient(uri)
        db = client["stock_db"]
        print("✅ Successfully connected to MongoDB Atlas!")
        return db["stock_col"], db["fo_col"]
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None, None
