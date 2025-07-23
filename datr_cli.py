# datr_cli.py

import sys
from src import lexer, parser, theory

def main():
    # Read input file
    if len(sys.argv) != 2:
        print("Usage: python datr_cli.py <input_file.dtr>")
        return

    # Open the input file
    filename = sys.argv[1]
    try:
        with open(filename, 'r',  encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Tokenize the file content
    print("== Tokens ==")
    lexer.lexer.input(data)
    for tok in lexer.lexer:
        print(tok)

    # Parse the file content
    print("\n== Parse Tree ==")
    result = parser.parser.parse(data, lexer=lexer.lexer)
    print(result)

    print("\n")
    datr_theory = theory.Theory("default", result)
    print(datr_theory.present())
    print("\n")
    # Enables the user to perform multiple queries at once, as long as the program doesn't crash
    while True:
        results = []
        user_input = input("Please input your prompt: ")
        queries = user_input.split(",")
        queries = [query.strip() for query in queries]
        print("Starting resolvement for queries: " + str(queries))
        for query in queries:
            results.append(datr_theory.query(query))
        print(prettify(results))

def compile_theory(filename):
    # Open the input file
    try:
        with open(filename, 'r',  encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Tokenize the file content
    print("== Tokens ==")
    lexer.lexer.input(data)
    for tok in lexer.lexer:
        print(tok)

    # Parse the file content
    print("\n== Parse Tree ==")
    result = parser.parser.parse(data, lexer=lexer.lexer)
    print(result)

    print("\n")
    return theory.Theory("default", result)

def prettify(result_list):
    pretty_list = []
    for result in result_list:
        pretty_entry = ""
        for element in result:
            pretty_entry += element
        pretty_list.append(pretty_entry)
    return pretty_list

if __name__ == '__main__':
    main()
