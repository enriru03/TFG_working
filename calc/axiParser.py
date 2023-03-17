# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:33:00 2023

@author: enriq
"""

# -----------------------------------------------------------------------------
# axiParser.py
#
# Parseador para fw de generacion de modulos axi. 
# Versión 1.0
# 
# Autor: Enrique Ruiz Santos
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input
    
#De momento es case sensitive: puedo hacerlo que no sea?
reserved = (
    'DEFINE', 'END', 'PARAMETERS', 'ARCHITECTURE', 'input', 'output', 
    'width', 'node', 'edge', 'connect', 'this',    
)

tokens = reserved + (
    
    #Entities to be recognised
    'MOD_NAME',
    'NUMBER',
    'IN_PORT',
    'OUT_PORT',
    'ID',
    
    #For symbols used in the gramar
    'EQUALS',
    'LPAREN', 
    'RPAREN', 
    'LKEY',
    'RKEY',
    'COLON',
    'COMA',
    'COMMENT',
)

# Tokens
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_COMA = r','
t_COLON = r':'

reserved_map = {}
for r in reserved:
    # reserved_map[r.lower()] = r
    reserved_map[r] = r
    
def t_MOD_NAME(t):
    r'axis_[a-zA-Z_][a-zA-Z0-9_]*'
    return t

#No debe reconocer esto si esta en un MOD_NAME o ID: OK -- EL punto es parte del token
#Deberia reconocer que numero de puerto es
def t_IN_PORT(t):
    r'\.in[0-9]+'
    return t

#Deberia reconcer que numero de puerto es: con t.value?
def t_OUT_PORT(t):
    r'\.out[0-9]+'
    return t

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_COMMENT(t):
    r'\#.*'
    pass
    #No devuelvo valor: descarto el resto de la linea

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    


# Build the lexer
import ply.lex as lex
lexer = lex.lex()

data = '''
DEFINE	axis_acc_squares {
	
	PARAMETERS:
	
		input = 1
		output = 1
		width = 32
	
	ARCHITECTURE:
		
		node split = axis_splitter_2(32)
		edge aristaA(32)
		connect (split.out1, aristaA)
		
} END axis_acc_squares
'''
# =============================================================================
# TO DO:
#     - Reconocer puertos
#  OK - this.input o decidir cómo hacerlo ---OK: source y sink como connect especiales
#  OK - Especificar comentarios -----OK
# =============================================================================

# =============================================================================
# lexer.input(data)
# 
# for tok in lexer:
#     print(tok)
# =============================================================================



# =============================================================================
# # Parsing rules
# =============================================================================

# dictionary of names: Para almacenar mis ID
# Usaré diccionarios distintos para mods y edges
# names = {}


# =============================================================================
#   PARSEADOR: 
# =============================================================================
# EXPRESIONES A RECONOCER: (No definitivo)
#     DEFINICION DE MODULO: (GLOBAL) : DEFINE MOD_NAME { TODO } END MOD_NAME
#     INSTANCIACION DE MODULO : module idModule = axiMODULE.  (axiMODULE : MOD_NAME() | MOD_NAME(NUMBER))
#     INSTANCIACIÖN DE ARISTA: edge idArista() | idArista(NUMBER)
#     CONNECT: connect    ( idModule OUT_PORT , idArista )
#                     |   ( idArista, idModule IN_PORT )
#                     |   ( this IN_PORT, idModule IN_PORT)
#                     |   ( idModule OUT_PORT, this IN_PORT)
# =============================================================================
    

def p_full_module(p):
    '''creation : define_module set_parameters set_architecture end_module'''

    print("full_module: ultima accion")
    
def p_define_module(p):
    'define_module : DEFINE MOD_NAME LKEY'
    print("Creacion de modulo: ")

def p_end_module(p):
    'end_module : RKEY END MOD_NAME'
    print("Terminacion de modulo: ")
 
#El orden debe ser intercambiable
def p_set_parameters(p):
    '''set_parameters : PARAMETERS COLON input EQUALS NUMBER output EQUALS NUMBER width EQUALS NUMBER'''
                            
    print('Set de parametros:')

def p_set_architecture(p):
    '''set_architecture : ARCHITECTURE COLON arch_expresions'''
    
    print("p_arch_expresionss")
    
def p_architecture_expresions(p):
    '''arch_expresions : arch_expresion
                      | arch_expresions arch_expresion '''
                      
    print("p_arch_expresions")
                       
def p_arch_expresion(p):
    '''arch_expresion : node_exp
                      | edge_exp
                      | connect_exp'''
     
    print("p_arch_expresion")
            
#De momento es obligatorio expresar la anchura al crear un nodo instanciando una axi_module
def p_new_node(p):
    '''node_exp : node ID EQUALS MOD_NAME LPAREN NUMBER RPAREN'''
    
    print("p_new_node")
    #Creo un objeto(?) nodo del tipo axi_module indicado. Tiene los puertos por definir
                       
def p_new_edge(p):
    '''edge_exp : edge ID LPAREN NUMBER RPAREN'''
    
    print("p_new_edge")
    #Creo un objeto(?) arista con la anchura indicada. Tiene la entrada y salida por definir

def p_connect_outport(p):
    'connect_exp : connect LPAREN ID OUT_PORT COMA ID RPAREN'
    
    print("p_connect_outport")
    #node ID(p[2]) outport = edge ID(p[5])
    
def p_connect_inport(p):
    'connect_exp : connect LPAREN ID COMA ID IN_PORT RPAREN'
    
    print("p_connect_inport")
    #node ID(p[4]) inport = edge ID(p[2])
    
def p_connect_module_input(p):
    'connect_exp : connect LPAREN this IN_PORT COMA ID IN_PORT RPAREN'
    
    print("p_connect_module_output")
    #node ID(p[5]) inport = module input
    
def p_connect_module_output(p):
    'connect_exp : connect LPAREN ID OUT_PORT COMA this OUT_PORT RPAREN'
    
    print("p_connect_module_imput")
    #node ID(p[5]) inport = module input    

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc(debug=True)



yacc.parse(data)

"""while 1:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
"""
