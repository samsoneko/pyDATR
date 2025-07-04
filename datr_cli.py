# datr_cli.py

import sys
from src import lexer, parser, theory

def main():
    # Read input file
    if len(sys.argv) != 3:
        print("Usage: python datr_cli.py <input_file.dtr> <query>")
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
    query = sys.argv[2]
    result = datr_theory.query(query)
    # # result = datr_theory.query("S1:<subj 1 sg futr obj 2 sg like>")
    print(result)

if __name__ == '__main__':
    main()
