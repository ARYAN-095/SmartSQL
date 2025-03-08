# Import necessary libraries
import json
import requests
import time
from database import DatabaseManager
from query_generator import SQLGenerator
from error_corrector import ErrorCorrector
from typing import List, Dict, Tuple

# Global variable to keep track of the total number of tokens
total_tokens = 0

# Function to load input file
def load_input_file(file_path: str) -> List[Dict]:
    """
    Load input file which is a list of dictionaries.
    
    :param file_path: Path to the input file
    :return: List of dictionaries
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []

# Function to generate SQL statements
def generate_sqls(data: List[Dict]) -> List[Dict]:
    """
    Generate SQL statements from the NL queries.
    
    :param data: List of NL queries
    :return: List of SQL statements
    """
    sql_statements = []
    db = DatabaseManager()
    generator = SQLGenerator()
    schema = db.get_schema()

    for item in data:
        nl_query = item.get("NL", "")
        generated_sql = generator.generate_sql(nl_query, schema)
        sql_statements.append({
            "NL": nl_query,
            "Query": generated_sql
        })
    
    return sql_statements

# Function to correct SQL statements
def correct_sqls(data: List[Dict]) -> List[Dict]:
    """
    Correct SQL statements if necessary.
    
    :param data: List of Dict with incorrect SQL statements and NL query
    :return: List of corrected SQL statements
    """
    corrected_sqls = []
    db = DatabaseManager()
    corrector = ErrorCorrector()
    schema = db.get_schema()

    for item in data:
        incorrect_sql = item.get("IncorrectQuery", "")
        nl_query = item.get("NL", "")
        corrected_sql = corrector.correct_sql(incorrect_sql, nl_query, schema)
        corrected_sqls.append({
            "IncorrectQuery": incorrect_sql,
            "CorrectQuery": corrected_sql
        })
    
    return corrected_sqls

# Function to call the Groq API
def call_groq_api(api_key: str, model: str, messages: List[Dict], temperature: float = 0.0, max_tokens: int = 1000, n: int = 1) -> Tuple[Dict, int]:
    """
    NOTE: DO NOT CHANGE/REMOVE THE TOKEN COUNT CALCULATION 
    Call the Groq API to get a response from the language model.
    :param api_key: API key for authentication
    :param model: Model name to use
    :param messages: List of message dictionaries
    :param temperature: Temperature for the model
    :param max_tokens: Maximum number of tokens to generate (these are max new tokens)
    :param n: Number of responses to generate
    :return: Response from the API
    """
    global total_tokens
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "messages": messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'n': n
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # Update the global token count
    total_tokens += response_json.get('usage', {}).get('completion_tokens', 0)

    # You can get the completion from response_json['choices'][0]['message']['content']
    return response_json, total_tokens

# Main function
def main() -> Tuple[float, float]:
    # Specify the path to your input file
    input_file_path_1 = 'data/input_file_for_sql_generation.json'
    input_file_path_2 = 'data/input_file_for_sql_correction.json'
    
    # Load data from input file
    data_1 = load_input_file(input_file_path_1)
    data_2 = load_input_file(input_file_path_2)
    
    if not data_1 or not data_2:
        print("Error: Input files are empty or invalid. Exiting.")
        return 0, 0
    
    start = time.time()
    # Generate SQL statements
    sql_statements = generate_sqls(data_1)
    generate_sqls_time = time.time() - start
    
    start = time.time()
    # Correct SQL statements
    corrected_sqls = correct_sqls(data_2)
    correct_sqls_time = time.time() - start
    
    assert len(data_2) == len(corrected_sqls) # If no answer, leave blank
    assert len(data_1) == len(sql_statements) # If no answer, leave blank
    
    # Save the outputs
    with open('output_sql_correction_task.json', 'w') as f:
        json.dump(corrected_sqls, f)    
    
    with open('output_sql_generation_task.json', 'w') as f:
        json.dump(sql_statements, f)
    
    return generate_sqls_time, correct_sqls_time

if __name__ == "__main__":
    generate_sqls_time, correct_sqls_time = main()
    print(f"Time taken to generate SQLs: {generate_sqls_time} seconds")
    print(f"Time taken to correct SQLs: {correct_sqls_time} seconds")
    print(f"Total tokens: {total_tokens}")