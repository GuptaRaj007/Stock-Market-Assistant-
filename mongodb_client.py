from pymongo import MongoClient, errors
from urllib.parse import quote_plus
import streamlit as st

# Securely load MongoDB credentials from Streamlit secrets (flat keys)
db_user_raw = st.secrets["MONGO_DB_USER"]
db_password_raw = st.secrets["MONGO_DB_PASSWORD"]

# URL encode credentials in case they have special chars
db_user = quote_plus(db_user_raw)
db_password = quote_plus(db_password_raw)

# Replace <your-cluster-url> below with the exact connection string host from Atlas
# For example: cluster0.xx3zem0.mongodb.net or ac-s9zuevw-shard-00-00.xx3zem0.mongodb.net
cluster_host = "cluster0.xx3zem0.mongodb.net"

# Construct MongoDB connection URI with explicit TLS
uri = (
    f"mongodb+srv://{db_user}:{db_password}@{cluster_host}/"
    "?retryWrites=true&w=majority&tls=true&appName=StreamlitStockApp"
)

def get_mongo_collection():
    """
    Connects to MongoDB Atlas cluster and returns references to
    the two collections: 'stock_col' and 'fo_col' in 'stock_db' database.
    """

    try:
        client = MongoClient(
            uri,
            tls=True,
            tlsAllowInvalidCertificates=False,  # Enforce proper cert validation
            serverSelectionTimeoutMS=5000,      # 5 seconds timeout
            connectTimeoutMS=10000               # 10 seconds connect timeout
        )

        # Test connection on client creation - forces server selection
        client.admin.command('ping')

        db = client["stock_db"]
        return db["stock_col"], db["fo_col"]

    except errors.ServerSelectionTimeoutError as e:
        st.error(f"Could not connect to MongoDB server: {e}")
        return None, None

    except Exception as e:
        st.error(f"Unexpected error connecting to MongoDB: {e}")
        return None, None
