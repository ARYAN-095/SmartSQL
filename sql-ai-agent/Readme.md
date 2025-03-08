                            
 # AI-Powered SQL Query Generator
 
This project is an AI-powered SQL query generator and error corrector designed to simplify database querying for non-technical users. It converts natural language queries into accurate SQL queries, handles errors, and provides corrected SQL when necessary. The system is optimized for enterprise environments with complex schemas and large datasets.

 
1. Problem  
Challenge: Writing SQL queries for complex databases is time-consuming and error-prone, especially for non-technical users.

Solution: Use AI to generate SQL queries from natural language inputs and automatically correct errors.

2.Key Features
Natural Language to SQL: Converts user queries into SQL using AI.

Error Correction: Detects and fixes SQL syntax and logical errors.

Schema Awareness: Understands database schema and relationships.

Optimized for 7B Models: Efficiently works within token limits for smaller AI models.

# Workflow
User provides a natural language query.

System generates SQL using the database schema and AI model.

Executes the query and validates results.

If errors occur, corrects the SQL and retries.

Returns the final SQL and results.





# Tech Stack

1. Core Technologies
Programming Language: Python

Database: PostgreSQL

AI Model: Groq API (7B parameter model)

Libraries:

psycopg2: PostgreSQL database connection

python-dotenv: Environment variable management

tabulate: Result formatting

json: Output serialization

 

# Low-Level Design (LLD)

1. Component Diagram

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


3.Future Enhancements
Support for more database systems (MySQL, SQL Server).

Advanced query optimization techniques.

Integration with BI tools for visualization.

User-friendly web interface.