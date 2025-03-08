from groq import Groq
from config import Config

class ErrorCorrector:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.system_prompt = """Fix SQL errors following these rules:
1. Preserve original intent
2. Return ONLY corrected SQL
3. Explain error in comments
4. Use PostgreSQL syntax
5. Handle schema mismatches
Schema: {schema}
Error: {error}"""

    def correct_sql(self, bad_sql: str, error: str, schema: str) -> str:
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": self.system_prompt.format(schema=schema, error=error)},
                {"role": "user", "content": bad_sql}
            ],
            temperature=0.1,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()