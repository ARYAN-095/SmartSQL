from database import DatabaseManager
from query_generator import SQLGenerator
from error_corrector import ErrorCorrector
import psycopg2
from typing import Tuple, Any
from tabulate import tabulate

class AIQueryAssistant:
    def __init__(self):
        self.db = DatabaseManager()
        self.generator = SQLGenerator()
        self.corrector = ErrorCorrector()
        self.schema = self.db.get_schema()
        
    def execute_query(self, query: str) -> Tuple[bool, Any]:
        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                self.db.conn.commit()
                return True, results
        except Exception as e:
            return False, str(e)
            
    def process_request(self, nl_query: str) -> dict:
        generated_sql = self.generator.generate_sql(nl_query, self.schema)
        success, result = self.execute_query(generated_sql)
        corrected_sql = None
        
        if not success:
            corrected_sql = self.corrector.correct_sql(generated_sql, str(result), self.schema)
            success, result = self.execute_query(corrected_sql)
            
        return {
            "nl_query": nl_query,
            "generated_sql": generated_sql,
            "corrected_sql": corrected_sql,
            "success": success,
            "result": result
        }

def print_test_result(result):
    print(f"\n{'=' * 50}")
    print(f"Natural Language Query:\n{result['nl_query']}")
    print(f"\nGenerated SQL:\n{result['generated_sql']}")
    
    if result['corrected_sql']:
        print(f"\nCorrected SQL:\n{result['corrected_sql']}")
    
    print(f"\nExecution Status: {'Success' if result['success'] else 'Failed'}")
    
    if result['success'] and result['result']:
        print("\nQuery Results:")
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
        print(tabulate(result['result'][:5], headers=headers, tablefmt="psql"))
    elif not result['success']:
        print(f"\nError: {result['result']}")
    
    print(f"{'=' * 50}\n")

if __name__ == "__main__":
    assistant = AIQueryAssistant()
    test_cases = [
        {
            "name": "Premium Customers in NY",
            "query": "Show me all premium customers from New York with loyalty points over 1000"
        },
        {
            "name": "Campaign Conversion Analysis",
            "query": """Compare conversion rates of summer sale campaigns 
                      for customers aged 25-35 vs 36-45 in different regions"""
        },
        {
            "name": "Inventory Restocking Alert",
            "query": """List products needing restocking (quantity below threshold) 
                      from Chinese suppliers with average rating above 4.5"""
        },
        {
            "name": "Revenue by Gender (Error Test)",
            "query": "Show total revenue by customer gender for electronics category"
        }
    ]

    try:
        for idx, test in enumerate(test_cases, 1):
            print(f"\n{'#' * 50}")
            print(f"Running Test Case {idx}: {test['name']}")
            result = assistant.process_request(test['query'])
            print_test_result(result)
    except Exception as e:
        print(f"Critical Error: {str(e)}")
    finally:
        assistant.db.conn.close()
        print("Database connection closed.")