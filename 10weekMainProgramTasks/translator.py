from openai import OpenAI
from pyswip import Prolog
import os

client = OpenAI(api_key="-")
prolog = Prolog()

def translate_to_prolog(natural_language, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Translate natural language to Prolog code, focusing on facts and rules about historical figures in computing."},
            {"role": "user", "content": f"Translate to Prolog: {natural_language}"}
        ]
    )
    return response.choices[0].message.content.strip()

def clean_and_assert_prolog(prolog_code):
    cleaned_lines = [line.strip() for line in prolog_code.split('\n') if line.strip() and not line.strip().startswith(('%', '`'))]
    for statement in cleaned_lines:
        statement = statement if statement.endswith('.') else statement + '.'
        print(f"Asserting: {statement}")
        prolog.assertz(statement)

def query_prolog(query):
    try:
        results = list(prolog.query(query))
        return results if results else "No results found."
    except Exception as e:
        return f"Error executing query: {str(e)}"

def process_natural_language(input_text, is_query=False):
    if is_query:
        prolog_query = translate_to_prolog(f"Translate this query to Prolog: {input_text}")
        return query_prolog(prolog_query)
    else:
        prolog_code = translate_to_prolog(input_text)
        clean_and_assert_prolog(prolog_code)
        return "Knowledge added to Prolog database."

def main():
    print("NLP-Prolog Integration System!")
    print("Add knowledge or ask questions about historical figures in computing.")
    
    while True:
        user_input = input("\nEnter your statement or query (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        is_query = input("Is this a query? (y/n): ").lower() == 'y'
        result = process_natural_language(user_input, is_query)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()