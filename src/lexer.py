import ply.lex as lex

# Reserved keywords
reserved = {
    '#atom': 'ATOM_EX',
    '#node': 'NODE_EX',
    '#vars': 'VARS',
}

# List of token names
tokens = [
    'COLON', 'EQ', 'DEFEQ', 'DOT',
    'L_ANGLE', 'R_ANGLE', 'L_ANGLE_LEFT', 'R_ANGLE_LEFT', 'L_PAREN', 'R_PAREN',
    'VARIABLE', 'NODE', 'ATOM', 'DQUOTE'
] + list(reserved.values())

# Ignore all comments (lines starting with #) in the file
def t_comment(t):
    r'%.*(?=\n)'
    pass

# Regular expressions for simple symbols
# These are reserved symbols for the syntax of DATR
t_COLON    = r':' # : | Separates node name and following content in a sentence
t_DEFEQ    = r'==' # == | Definitional statement expression
t_EQ       = r'=' # = | Extensional statement expression
t_DOT      = r'\.' # . | Each node definition ends with a dot after the last expression
t_L_ANGLE   = r'<' # < | Marks beginning of path expression (all except ones on the left side)
t_R_ANGLE   = r'>' # > | Marks end of path expression (all except ones on the left side)
t_L_ANGLE_LEFT = r"<(?=(?:'[^']*'|[^<>'])*>\s*=)" # < | Marks beginning of path expression on the left
t_R_ANGLE_LEFT = r'>(?=\s*=)' # < | Marks beginning of path expression on the left
t_L_PAREN   = r'\(' # ( | Opening parenthesis
t_R_PAREN   = r'\)' # ) | Closing parenthesis
# # | Used for definitions
# $ | Used for variables
t_DQUOTE    = r'"' # " | Used for global inheritance
# ' | Single quotation mark

# Ignore whitespace and tabs
t_ignore = ' \t\r'

def t_VARIABLE(t):
    r"\$[^\W!:<>\(\)=\"'\.%]+" # Regex for variables, need to start with $, otherwise free
    return t

def t_NODE(t):
    r"[A-ZÀ-ÖØ-Þ][^\W!:<>\(\)=\"'\.%]*" # Regex for names of nodes, needs to start with capital letter, otherwise free
    return t

def t_ATOM(t):
    r"[^\WA-Z!:<>\(\)=\"'\.%][^\W!:<>\(\)=\"'\.%]*" # Regex for atom content, not allowed to start with an uppercase letter, otherwise free
    return t

# def t_CHAR_STRING(t):
#     r'[a-zA-Z0-9_]+' # Regex for string of chars, relevant for ATOM_EX
#     return t

# def t_ANY_STRING(t):
#     r"'[^']*'" # Regex for any string of symbols
#     return t

def t_RESERVED(t):
    r'\#[a-z]+' # Regex for expressions starting with #
    t.type = reserved.get(t.value, 'RESERVED') # Get value from dictionary, otherwise return 'RESERVED'
    return t

def t_newline(t):
    r'\n+' # Regex for newline
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {t.value[0]!r}") # Fallback for all illegal tokens and chars
    t.lexer.skip(1)

lexer = lex.lex()