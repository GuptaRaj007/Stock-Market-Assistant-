import requests
import re
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
        stock_col, fo_col = get_mongo_collection()  # unpack both collections
        embedding = EmbeddingGenerator.generate(query)

        results = stock_col.aggregate([
            {
                "$vectorSearch": {
                    "queryVector": embedding,
                    "path": "embedding",
                    "numCandidates": 400,
                    "limit": 5,
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
        print(f"🚀 Executing method get_companies_by_result_date with query: \"{query}\"")

        # Get the collections
        print("🔗 Connecting to MongoDB and retrieving collections...")
        stock_col, fo_col = get_mongo_collection()

        # Extract result_date (YYYY-MM-DD format)
        print("🔎 Extracting result date from query...")
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
        if not date_match:
            print("❌ No valid date found in query.")
            return "❌ Invalid query. Please provide a date in YYYY-MM-DD format."
        result_date = date_match.group()
        print(f"✅ Extracted result date: {result_date}")

        # Extract F&O status (Yes or No)
        print("🔎 Checking for F&O status (Yes/No) in query...")
        fno_match = re.search(r'\b(yes|no)\b', query, re.IGNORECASE)
        part_of_fno = None
        if fno_match:
            part_of_fno = "Yes" if fno_match.group().lower() == "yes" else "No"
            print(f"✅ F&O filter extracted: {part_of_fno}")
        else:
            print("ℹ️ No F&O filter provided in query.")

        # Build filter for stock_col
        mongo_filter = {"result_date": result_date}
        print(f"🔎 MongoDB filter for stock_col: {mongo_filter}")

        # Query stock_col
        print("📤 Querying stock_col collection...")
        stock_results = stock_col.find(mongo_filter)
        stock_results = list(stock_results)  # Convert cursor to list for multiple passes
        print(f"🔍 Found {len(stock_results)} documents matching result date.")

        companies = []
        for row in stock_results:
            company_name = row.get("company_name", "N/A")
            security_code = row.get("security_code", "N/A")
            security_name = row.get("security_name", "N/A")
            print(f"➡️ Processing company: {company_name}, Security Name: {security_name}")

            # Cross-check with fo_col (fo_stock) by matching symbol
            print(f"🔄 Checking if \"{security_name}\" is part of F&O...")
            fo_match = fo_col.find_one({"symbol": security_name})
            is_fno = bool(fo_match)
            print(f"📊 F&O Match: {'Yes' if is_fno else 'No'}")

            # Apply filter based on query's part_of_fno
            if part_of_fno:
                if (part_of_fno == "Yes" and not is_fno) or (part_of_fno == "No" and is_fno):
                    print(f"⏩ Skipping {company_name} due to F&O filter mismatch.")
                    continue

            f_o_symbol = fo_match['symbol'] if fo_match else "N/A"
            companies.append(
                f"{company_name} | Security Code: {security_code} | "
                f"F&O Symbol: {f_o_symbol} | Result Date: {result_date} | "
                f"F&O Status: {'Yes' if is_fno else 'No'}"
            )
            print(f"✅ Added company: {company_name}")

        if not companies:
            print("❌ No companies found after applying filters.")
            return f"No companies found matching query \"{query}\""

        result_output = (
                f"Companies matching \"{query}\":\n" +
                "\n".join(f"- {entry}" for entry in companies)
        )
        print("📢 Final result output prepared:\n" + result_output)
        return result_output
