from openai import OpenAI
from pyswip import Prolog

Client = OpenAI(api_key="-")

def translate_to_prolog(natural_language):
    response = Client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates natural language to Prolog code. Focus on representing facts and rules about historical figures in computing and their contributions."},
            {"role": "user", "content": f"Translate the following to Prolog, focusing on facts and rules about historical figures in computing: {natural_language}"}
        ]
    )
    return response.choices[0].message.content.strip()

def clean_prolog_code(prolog_code):
    lines = prolog_code.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('%') and not line.strip().startswith('`')]
    return cleaned_lines

def run_prolog(prolog, prolog_code):
    try:
        cleaned_code = clean_prolog_code(prolog_code)
        for statement in cleaned_code:
            if not statement.endswith('.'):
                statement += '.'  # Ensure each statement ends with a dot
            print(f"Asserting: {statement}")
            prolog.assertz(statement)
        return True, prolog
    except Exception as e:
        return False, str(e)

def query_prolog(prolog, query):
    try:
        results = list(prolog.query(query))
        return True, results
    except Exception as e:
        return False, str(e)

def main():
    natural_language = """
    Ada Lovelace was a mathematician and writer in the 19th century.
    She is often regarded as the first computer programmer.
    Lovelace worked on Charles Babbage's proposed mechanical general-purpose computer, the Analytical Engine.
    She published the first algorithm intended to be carried out by such a machine.
    Her notes on the Analytical Engine include what is recognized as the first computer program.
    Lovelace also theorized a method for the engine to repeat a series of instructions, a process known as looping that computer programs use today.
    Define rules to determine if someone is a pioneer in computer science based on their early contributions to the field.
    """

    print(f"Natural Language Input:\n{natural_language}")

    prolog_code = translate_to_prolog(natural_language)
    print(f"\nTranslated Prolog Code:\n{prolog_code}")

    prolog = Prolog()
    success, prolog_or_error = run_prolog(prolog, prolog_code)

    if success:
        print("\nProlog code parsed successfully.")
        query_success, results_or_error = query_prolog(prolog_or_error, "pioneer_in_computer_science(ada_lovelace).")
        if query_success:
            if results_or_error:
                print("Query result: Ada Lovelace is considered a pioneer in computer science.")
            else:
                print("Query result: Ada Lovelace is not considered a pioneer in computer science based on the given rules.")
        else:
            print(f"Error executing query: {results_or_error}")
    else:
        print(f"\nError parsing Prolog code: {prolog_or_error}")

if __name__ == "__main__":
    main()
