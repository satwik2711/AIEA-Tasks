import openai
from openai import OpenAI
from pyswip import Prolog

Client = OpenAI(api_key="--YOUR API")

def translate_to_prolog(natural_language):
    response = Client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates natural language to Prolog code. Focus on representing facts and rules about historical figures in computing and their contributions."},
            {"role": "user", "content": f"Translate the following to Prolog, focusing on facts and rules about historical figures in computing: {natural_language}"}
        ]
    )
    return response.choices[0].message.content

def clean_prolog_code(prolog_code):
    # Remove markdown code block markers and any text outside the Prolog code
    lines = prolog_code.split('\n')
    cleaned_lines = [line for line in lines if not line.startswith('```') and not line.startswith('The Prolog code')]
    return '\n'.join(cleaned_lines).strip()

def run_prolog(prolog_code):
    prolog = Prolog()
    try:
        prolog.assertz(prolog_code)
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
    
    success, prolog = run_prolog(prolog_code)
    
    if success:
        print("\nProlog code parsed successfully.")
        query_success, results = query_prolog(prolog, "pioneer_in_computer_science(ada_lovelace)")
        if query_success:
            if results:
                print("Query result: Ada Lovelace is considered a pioneer in computer science.")
            else:
                print("Query result: Ada Lovelace is not considered a pioneer in computer science based on the given rules.")
        else:
            print(f"Error executing query: {results}")
    else:
        print(f"\nError parsing Prolog code: {prolog}")

if __name__ == "__main__":
    main()