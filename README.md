AI-Powered SQL Query Generator
Overview
This project is an AI-powered SQL query generator and error corrector designed to simplify database querying for non-technical users. It converts natural language queries into accurate SQL queries, handles errors, and provides corrected SQL when necessary. The system is optimized for enterprise environments with complex schemas and large datasets.

Approach
1. Problem Understanding
Challenge: Writing SQL queries for complex databases is time-consuming and error-prone, especially for non-technical users.

Solution: Use AI to generate SQL queries from natural language inputs and automatically correct errors.

2. Key Features
Natural Language to SQL: Converts user queries into SQL using AI.

Error Correction: Detects and fixes SQL syntax and logical errors.

Schema Awareness: Understands database schema and relationships.

Optimized for 7B Models: Efficiently works within token limits for smaller AI models.

3. Workflow
User provides a natural language query.

System generates SQL using the database schema and AI model.

Executes the query and validates results.

If errors occur, corrects the SQL and retries.

Returns the final SQL and results.

Tech Stack
1. Core Technologies
Programming Language: Python

Database: PostgreSQL

AI Model: Groq API (7B parameter model)

Libraries:

psycopg2: PostgreSQL database connection

python-dotenv: Environment variable management

tabulate: Result formatting

json: Output serialization

2. Key Components
Database Manager: Handles schema extraction and query execution.

SQL Generator: Converts natural language to SQL using AI.

Error Corrector: Fixes SQL errors using AI.

Query Executor: Validates and executes SQL queries.

Low-Level Design (LLD)
1. Component Diagram
Copy
+-------------------+       +-------------------+       +-------------------+
|   User Input      |       |   SQL Generator   |       |   Error Corrector  |
|  (Natural Lang)   | ----> |  (AI-Powered)     | ----> |  (AI-Powered)      |
+-------------------+       +-------------------+       +-------------------+
        |                           |                           |
        v                           v                           v
+-------------------+       +-------------------+       +-------------------+
|   Database Schema |       |   Query Executor  |       |   Output Formatter |
|  (PostgreSQL)     | <---- |  (Validation)    | <---- |  (JSON/Table)      |
+-------------------+       +-------------------+       +-------------------+
2. Data Flow
Input: User provides a natural language query.

Schema Extraction: Database schema is fetched and optimized for token efficiency.

SQL Generation: AI model generates SQL based on the query and schema.

Execution: Query is executed on the database.

Error Handling: If execution fails, the error is corrected using AI.

Output: Results are formatted and saved as JSON.

3. Class Diagram
plaintext
Copy
+---------------------+
|   AIQueryAssistant  |
+---------------------+
| - db: DatabaseManager
| - generator: SQLGenerator
| - corrector: ErrorCorrector
| - schema: str
+---------------------+
| + execute_query()
| + process_request()
+---------------------+

+---------------------+
|   DatabaseManager   |
+---------------------+
| - conn: psycopg2.connection
+---------------------+
| + get_schema()
| + execute_query()
+---------------------+

+---------------------+
|   SQLGenerator      |
+---------------------+
| - client: Groq
+---------------------+
| + generate_sql()
+---------------------+

+---------------------+
|   ErrorCorrector    |
+---------------------+
| - client: Groq
+---------------------+
| + correct_sql()
+---------------------+
4. Sequence Diagram
plaintext
Copy
User -> AIQueryAssistant: Natural Language Query
AIQueryAssistant -> DatabaseManager: Fetch Schema
DatabaseManager --> AIQueryAssistant: Schema
AIQueryAssistant -> SQLGenerator: Generate SQL
SQLGenerator --> AIQueryAssistant: SQL Query
AIQueryAssistant -> DatabaseManager: Execute Query
DatabaseManager --> AIQueryAssistant: Results/Error
alt Error Occurred
    AIQueryAssistant -> ErrorCorrector: Correct SQL
    ErrorCorrector --> AIQueryAssistant: Corrected SQL
    AIQueryAssistant -> DatabaseManager: Execute Corrected Query
    DatabaseManager --> AIQueryAssistant: Results
end
AIQueryAssistant -> Output Formatter: Format Results
Output Formatter --> User: JSON Output
How to Run
1. Setup
Install dependencies:

bash
Copy
pip install -r requirements.txt
Configure .env file:

env
Copy
DB_HOST=localhost
DB_NAME=hackathon_iitd
DB_USER=your_username
DB_PASSWORD=your_password
GROQ_API_KEY=your_groq_key
Import database schema:

bash
Copy
psql -d hackathon_iitd -f hackathon_database_iitd.sql
2. Execution
Run the application:

bash
Copy
python app.py
3. Output
Results are saved in output.json.

Sample output:

json
Copy
[
  {
    "test_case": "Premium Customers in NY",
    "timestamp": "2024-01-20T15:30:45.123456",
    "nl_query": "Show me all premium customers from New York...",
    "generated_sql": "SELECT * FROM customerInfo...",
    "corrected_sql": null,
    "execution_success": true,
    "results": [["John", "Doe", "john.doe@email.com"]],
    "error": null
  }
]
Evaluation Metrics
SQL Accuracy: Correctness of generated SQL.

Output Accuracy: Correctness of query results.

Execution Success Rate: Ratio of successfully executed queries.

Token Efficiency: Cost-effectiveness in generating results.

Time Efficiency: Total execution time across test cases.

Future Enhancements
Support for more database systems (MySQL, SQL Server).

Advanced query optimization techniques.

Integration with BI tools for visualization.

User-friendly web interface.
