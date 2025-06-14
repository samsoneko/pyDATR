import ply.yacc as yacc
from src.lexer import tokens

# --- AST Nodes / Output Builders ---

def p_theory_multiple(p):
    '''theory : statement theory'''
    p[0] = [p[1]] + p[2]

def p_theory_single(p):
    '''theory : statement'''
    p[0] = [p[1]]

# --- Statements ---

# def p_statement_atom(p):
#     '''statement : ATOM_EX itemlist DOT'''
#     p[0] = ('atom_exceptions', p[2])

# def p_statement_node(p):
#     '''statement : NODE_EX itemlist DOT'''
#     p[0] = ('node_exceptions', p[2])

def p_statement_vars(p):
    '''statement : VARS VARIABLE COLON atomlist DOT'''
    p[0] = ('variables', p[2], p[4])

def p_statement_sentence(p):
    '''statement : NODE COLON eqseq DOT'''
    p[0] = ('node', p[1], p[3])

# --- Itemlists and Strings ---

# def p_itemlist_multiple(p):
#     '''itemlist : item itemlist'''
#     p[0] = [p[1]] + p[2]

# def p_itemlist_single(p):
#     '''itemlist : item'''
#     p[0] = [p[1]]

# def p_item(p):
#     '''item : CHAR_STRING | ANY_STRING'''
#     p[0] = p[1].strip("'")

# --- Atomlist ---

def p_atomlist_multiple(p):
    '''atomlist : ATOM atomlist'''
    p[0] = [p[1]] + p[2]

def p_atomlist_single(p):
    '''atomlist : ATOM'''
    p[0] = [p[1]]

# --- Equation Sequences ---

def p_eqseq_multiple(p):
    '''eqseq : equation eqseq'''
    p[0] = [p[1]] + p[2]

def p_eqseq_single(p):
    '''eqseq : equation'''
    p[0] = [p[1]]

def p_equation(p):
    '''equation : lhs rhs'''
    p[0] = ('equation', p[1], p[2])

# --- Left-hand side ---

def p_lhs(p):
    '''lhs : L_ANGLE_LEFT atomseq R_ANGLE_LEFT'''
    p[0] = ('lhs', p[2])

# --- Right-hand side (value) ---

def p_rhs_extrhs(p):
    '''rhs : EQ atomval'''
    p[0] = ('extensional', p[2])

def p_rhs_defrhs(p):
    '''rhs : DEFEQ descval'''
    p[0] = ('definitional', p[2])

# --- Atom values ---

def p_atomval_plain(p):
    '''atomval : atomseq'''
    p[0] = p[1]

def p_atomval_paren(p):
    '''atomval : L_PAREN atomseq R_PAREN'''
    p[0] = p[2]

def p_atomseq_multiple(p):
    '''atomseq : ATOM atomseq'''
    p[0] = [p[1]] + p[2]

def p_atomseq_empty(p):
    '''atomseq : '''
    p[0] = []

# --- Desc values ---

def p_descval_plain(p):
    '''descval : descseq'''
    p[0] = p[1]

def p_descval_paren(p):
    '''descval : L_PAREN descseq R_PAREN'''
    p[0] = p[2]

def p_descseq_multiple(p):
    '''descseq : desc descseq'''
    p[0] = [p[1]] + p[2]

def p_descseq_empty(p):
    '''descseq : '''
    p[0] = []

# --- Descriptions (atoms or pointers) ---

def p_desc_atom(p):
    '''desc : ATOM'''
    p[0] = p[1]

def p_desc_pointer_dquoted(p):
    '''desc : DQUOTE pointer DQUOTE'''
    p[0] = ('global_pointer', p[2])

def p_desc_pointer(p):
    '''desc : pointer'''
    p[0] = p[1]

# --- Pointers and paths ---

def p_pointer_node_descpath(p):
    '''pointer : NODE COLON descpath'''
    p[0] = ('local_pointer', p[1], p[3])

def p_pointer_node(p):
    '''pointer : NODE'''
    p[0] = ('local_pointer', p[1], None)

def p_pointer_descpath(p):
    '''pointer : descpath'''
    p[0] = ('local_pointer', None, p[1])

def p_descpath(p):
    '''descpath : L_ANGLE descseq R_ANGLE'''
    p[0] = p[2]

# --- Error handling ---

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc(write_tables=False)