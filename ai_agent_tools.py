get_stock_live_data_tool = {
    'type': 'function',
    'function': {
        'name': 'get_stock_live_data',
        'description': 'Fetches live stock data including current price, high, low, open, and previous close using the stock ticker symbol.',
        'parameters': {
            'type': 'object',
            'properties': {
                'symbol': {
                    'type': 'string',
                    'description': 'Stock ticker symbol (e.g., AAPL, INFY, TCS.BSE)'
                }
            },
            'required': ['symbol']
        },
        'returns': {
            'type': 'string',
            'description': 'Formatted stock data including current, high, low, open, and previous close prices.'
        }
    }
}


get_stock_additional_info_tool = {
    'type': 'function',
    'function': {
        'name': 'get_stock_additional_info',
        'description': 'Fetches detailed stock information, including optional F&O data if available. Use exact security codes (e.g., HSC) for precise results. Returns company details and financial data.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'User query to identify the stock or company (e.g., "tell me about HSC").'
                }
            },
            'required': ['query'],
        },
        'returns': {
            'type': 'object',
            'properties': {
                'company_name': {'type': 'string', 'description': 'Company name'},
                'security_name': {'type': 'string', 'description': 'Security name of the stock'},
                'security_code': {'type': 'string', 'description': 'Security code listed on the exchange'},
                'fincode': {'type': 'string', 'description': 'Financial code of the stock'},
                'result_date': {'type': 'string', 'description': 'Date of quarterly/annual result declaration'},
                'quarter': {'type': 'string', 'description': 'Financial quarter (e.g., Q1, Q2)'},
                'quarter_year': {'type': 'string', 'description': 'Financial year of the result (e.g., 2024)'},
                'f_o_data': {
                    'type': 'object',
                    'description': 'Optional F&O market data if available',
                    'properties': {
                        'symbol': {'type': 'string', 'description': 'F&O symbol'},
                        'ltp': {'type': 'number', 'description': 'Last traded price'},
                        'open': {'type': 'number', 'description': 'Opening price'},
                        'high': {'type': 'number', 'description': 'Highest price'},
                        'low': {'type': 'number', 'description': 'Lowest price'}
                    },
                    'required': []
                }
            },
            'required': [
                'company_name', 'security_name', 'security_code', 'fincode',
                'result_date', 'quarter', 'quarter_year'
            ]
        }
    }
}


get_companies_by_result_date_tool = {
    'type': 'function',
    'function': {
        'name': 'get_companies_by_result_date',
        'description': (
            'Fetches companies based on result date and whether the company is part of F&O or not. '
            'The query should contain a date in YYYY-MM-DD format and optionally "Yes" or "No" to specify F&O participation.'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': (
                        'Query text containing the result date (YYYY-MM-DD) and optionally the F&O participation ("Yes" or "No"). '
                        'For example: "2025-01-13 F&O Yes"'
                    )
                }
            },
            'required': ['query']
        }
    }
}
