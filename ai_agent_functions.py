import requests
from mongodb_client import get_mongo_collection
from generate_embedding import EmbeddingGenerator

class Functions:
    @staticmethod
    def get_stock_live_data(symbol: str) -> str:
        response = requests.get(
            f"https://finnhub.io/api/v1/quote?symbol={symbol}&token=d03ii2pr01qh439h4l2gd03ii2pr01qh439h4l30"
        )
        data = response.json()
        return (
            f"Stock: {symbol}\n"
            f"Current: ${data['c']}, High: ${data['h']}, Low: ${data['l']}, "
            f"Open: ${data['o']}, Previous Close: ${data['pc']}"
        )

    @staticmethod
    def get_stock_additional_info(query: str) -> str:
        print("Executing method get_stock_additional_info")
        collection = get_mongo_collection()
        embedding = EmbeddingGenerator.generate(query)

        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "queryVector": embedding,
                    "path": "embedding",
                    "numCandidates": 400,
                    "limit": 1,
                    "index": "default",
                }
            }
        ])
        print('======================')
        print(results)
        print('======================')
        for row in results:
            response_parts = [
                f"Company Name: {row.get('company_name', 'N/A')}.",
                f"Security Name: {row.get('security_name', 'N/A')}.",
                f"Security Code: {row.get('security_code', 'N/A')}.",
                f"Fincode: {row.get('fincode', 'N/A')}.",
                f"Result Date: {row.get('result_date', 'N/A')}.",
                f"Quarter: Q{row.get('quarter', 'N/A')} of {row.get('quarter_year', 'N/A')}."
            ]

            # Optional F&O data
            f_o_data = row.get("f&o_data")
            if isinstance(f_o_data, dict):
                response_parts.append(
                    f"F&O Data - Symbol: {f_o_data.get('symbol', 'N/A')}, "
                    f"LTP: {f_o_data.get('ltp', 'N/A')}, "
                    f"Open: {f_o_data.get('open', 'N/A')}, "
                    f"High: {f_o_data.get('high', 'N/A')}, "
                    f"Low: {f_o_data.get('low', 'N/A')}."
                )
            print(" ".join(response_parts))
            return " ".join(response_parts)

        return "No relevant stock information found."

    @staticmethod
    def get_companies_by_result_date(query: str) -> str:
        print(f"Executing method get_companies_by_result_date with query: \"{query}\"")
        collection = get_mongo_collection()

        import re

        # Extract result_date (YYYY-MM-DD format)
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
        if not date_match:
            return "❌ Invalid query. Please provide a date in YYYY-MM-DD format."
        result_date = date_match.group()

        # Extract F&O status (Yes or No)
        fno_match = re.search(r'\b(yes|no)\b', query, re.IGNORECASE)
        part_of_fno = None
        if fno_match:
            part_of_fno = "Yes" if fno_match.group().lower() == "yes" else "No"

        # Build MongoDB filter
        mongo_filter = {"result_date": result_date}
        if part_of_fno:
            mongo_filter["part_of_fno"] = part_of_fno

        print(f"🔎 MongoDB filter: {mongo_filter}")

        # Query the database
        results = collection.find(mongo_filter).limit(5)

        companies = []
        for row in results:
            f_o_data = row.get("f&o_data")
            f_o_symbol = f_o_data.get('symbol', 'N/A') if isinstance(f_o_data, dict) else 'N/A'

            companies.append(
                f"{row.get('company_name', 'N/A')} | Security Code: {row.get('security_code', 'N/A')} | "
                f"F&O Symbol: {f_o_symbol} | Result Date: {row.get('result_date', 'N/A')}"
            )

        if not companies:
            return f"No companies found matching query \"{query}\""
        print((
                f"Companies matching \"{query}\":\n" +
                "\n".join(f"- {name}" for name in companies)
        ))
        return (
                f"Companies matching \"{query}\":\n" +
                "\n".join(f"- {name}" for name in companies)
        )
