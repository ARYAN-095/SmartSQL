from groq import Groq
from config import Config
import json

class SQLGenerator:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.system_prompt = """You are a SQL expert. Generate PostgreSQL queries following these rules:
1. Use ONLY provided schema
2. Be concise
3. Return ONLY SQL, no explanations
4. Use standard SQL style
5. Prefer CTEs over subqueries
6. Handle nulls appropriately
Schema: {schema}"""

    def generate_sql(self, nl_query: str, schema: str) -> str:
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": self.system_prompt.format(schema=schema)},
                {"role": "user", "content": nl_query}
            ],
            temperature=0.1,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()