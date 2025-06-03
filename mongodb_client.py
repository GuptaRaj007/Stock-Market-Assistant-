from pymongo import MongoClient
from urllib.parse import quote_plus
import streamlit as st

db_user_raw = st.secrets["MONGO"]["MONGO_DB_USER"]
db_password_raw = st.secrets["MONGO"]["MONGO_DB_PASSWORD"]

db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.xx3zem0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"

def get_mongo_collection():
    client = MongoClient(
        uri,
        tls=True,
        tlsAllowInvalidCertificates=False,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
    )
    db = client["stock_db"]
    return db["stock_col"], db["fo_col"]
