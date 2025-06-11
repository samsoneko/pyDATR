# main.py

import sys
from src import lexer, parser, theory

def main():
    # Read input file
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file.datr>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r',  encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Tokenize (optional debug step)
    print("== Tokens ==")
    lexer.lexer.input(data)
    for tok in lexer.lexer:
        print(tok)

    # Parse
    print("\n== Parse Tree ==")
    result = parser.parser.parse(data, lexer=lexer.lexer)
    print(result)

    datr_theory = theory.build_theory(result)
    print(datr_theory)

if __name__ == '__main__':
    main()
