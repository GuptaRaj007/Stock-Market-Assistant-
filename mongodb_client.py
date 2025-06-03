from pymongo import MongoClient
from urllib.parse import quote_plus
import streamlit as st

# Load credentials securely from Streamlit secrets
db_user_raw = st.secrets["MONGO_DB_USER"]
db_password_raw = st.secrets["MONGO_DB_PASSWORD"]

db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

# === CRITICAL: Use the exact cluster host from your Atlas connection string here ===
# It should match your error messages' shard hostname prefix, e.g. "ac-s9zuevw.xx3zem0.mongodb.net"
cluster_host = "ac-s9zuevw.xx3zem0.mongodb.net"  

# Add tls=true explicitly to force TLS
uri = (
    f"mongodb+srv://{db_user}:{db_password}@{cluster_host}/"
    "?retryWrites=true&w=majority&appName=Cluster0&tls=true"
)

def get_mongo_collection():
    client = MongoClient(uri)
    db = client["stock_db"]
    return db["stock_col"], db["fo_col"]
