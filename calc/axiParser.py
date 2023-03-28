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

#Tokens
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
		edge aristaB(32)
		connect(split.out1, aristaA)
		connect(split.out2, aristaB)
		
		node mult = axis_multiplier(32)
		connect(aristaA, mult.in1)
		connect(aristaB, mult.in2)
		edge aristaC(32)
		connect(mult.out1, aristaC)
		
        #Coemtnario de tal
        
		node acc = axis_accumulator(32)
		connect(aristaC, acc.in1)		
		
		
		connect(this.in1, split.in1) 
		connect(acc.out1, this.out1)

} END axis_acc_squares
'''
# =============================================================================
# TO DO:
#  - Reconocer puertos --- OK
#  - this.input o decidir cómo hacerlo ---OK: source y sink como connect especiales
#  - Especificar comentarios -----OK
#  - Leer input como in file .afw 
#  - Crear estructuras de objetos node y edge con atributos: 
#        - Que estructura y que objetos?
#        - En este mismo file?
#  - Permitir que se especifique o no la anchura de los node y edge
# =============================================================================
# =============================================================================
# TO DO_2:
#  - Posible problema: que llamen a una arista sourceN o sinkN
#  - Diccionarios para poder buscar por claves --- OK
#  - Leer archivo de entrada .afw
#  - Fexibilizar anchurs de node y edges
# =============================================================================

# =============================================================================
# lexer.input(data)
# 
# for tok in lexer:
#     print(tok)
# =============================================================================

# =============================================================================
# #Estructuras que crear y pasar
# =============================================================================
module = {}
module["edge_dict"] = {}
module["node_dict"] = {}
module["conn_dict"] = {}

# =============================================================================
# PARSER RULES AND ACTIONS:
# =============================================================================

def p_full_module(p):
    '''creation : define_module set_parameters set_architecture end_module'''

    print("full_module: ultima accion")
    
def p_define_module(p):
    'define_module : DEFINE MOD_NAME LKEY'
    print("Creacion de modulo: ")
    
    module["name"] = p[2]

def p_end_module(p):
    'end_module : RKEY END MOD_NAME'
    print("Terminacion de modulo: ")

#permito que el orden sea intercambiable
def p_set_parameters(p):
    '''set_parameters : PARAMETERS COLON parameters_exp parameters_exp parameters_exp'''
                            
    print('Set de parametros:')
    
def p_param_exp_input(p):
    '''parameters_exp : input EQUALS NUMBER'''
      
    #Como NUMBER.value si devuelve entero, puedo cogerlo directamente
    module["input"] = p[3]
    
    print("parameters input:", p[3])
    
def p_param_exp_output(p):
    '''parameters_exp : output EQUALS NUMBER'''
    
    module["output"] = p[3]
      
    print('parameters output:')
    
def p_param_exp_width(p):
    '''parameters_exp : width EQUALS NUMBER'''
    
    module["width"] = p[3]
    
    print('parameters width:')

def p_set_architecture(p):
    '''set_architecture : ARCHITECTURE COLON arch_expresions'''
    
    print("p_set_architecture")
 
    # Orden importante ?¿
def p_architecture_expresions(p):
    '''arch_expresions : arch_expresion
                      | arch_expresion arch_expresions'''
                      
    print("p_arch_expresionss")
                       
def p_arch_expresion(p):
    '''arch_expresion : node_exp
                      | edge_exp
                      | connect_exp'''
     
    print("p_arch_expresion")
            
#De momento es obligatorio expresar la anchura al crear un nodo instanciando una axi_module
def p_new_node(p):
    '''node_exp : node ID EQUALS MOD_NAME LPAREN NUMBER RPAREN'''
    
    #Aqui es donde leo la anchura por defecto si no hay ninguna: -- Meter w= 0 para que se
    # reconozca como default al crear el nodo
    
    module["node_dict"][p[2]] = {"node_type" : p[4], "width": p[6]}

    print("p_new_node")
    
                       
def p_new_edge(p):
    '''edge_exp : edge ID LPAREN NUMBER RPAREN'''
    
    #Aqui es donde leo la anchura por defecto si no hay ninguna: -- Meter w= 0 para que se
    # reconozca como default al crear la arista
    
    module["edge_dict"][p[2]] = p[4]
    
    print("p_new_edge")
    #Creo un objeto(?) arista con la anchura indicada. Tiene la entrada y salida por definir

def p_connect_outport(p):
    'connect_exp : connect LPAREN ID OUT_PORT COMA ID RPAREN'
    
    # p[3] = node_id
    port_name = "output_" + p[4][4:]
    edge_id = p[6] #Posible problema: que llamen a una arista sourceN o sinkN

  
    if p[3] in module["conn_dict"]:
        module["conn_dict"][p[3]].update({port_name: edge_id}) 
    else:
        module["conn_dict"][p[3]] = {port_name: edge_id}
    # module["conn_dict"][p[3]]={p[4]: p[6]}
    
    print("p_connect_outport")
    
def p_connect_inport(p):
    'connect_exp : connect LPAREN ID COMA ID IN_PORT RPAREN'
    
    # p[5] = node_id
    port_name = "input_" + p[6][3:]
    edge_id = p[3] #Posible problema: que llamen a una arista sourceN o sinkN
    
    if p[5] in module["conn_dict"]:
        module["conn_dict"][p[5]].update({port_name: edge_id}) 
    else:
        module["conn_dict"][p[5]] = {port_name: edge_id}
        
    print("p_connect_inport")
    
def p_connect_module_input(p):
    'connect_exp : connect LPAREN this IN_PORT COMA ID IN_PORT RPAREN'  
    
   
    
    # p[6] = node_id
    port_name = "input_" + p[7][3:]
    source_name = "source" + p[4][3:] 
    
    
    if p[6] in module["conn_dict"]:
        module["conn_dict"][p[6]].update({port_name: source_name}) 
    else:
        module["conn_dict"][p[6]] = {port_name: source_name}
    
    print("p_connect_module_output")
    #node ID(p[5]) inport = module input
    
def p_connect_module_output(p):
    'connect_exp : connect LPAREN ID OUT_PORT COMA this OUT_PORT RPAREN'
    
    
    
    # p[3] = node_id, p[4] = num_port, sink_name = sink+numport
    port_name = "output_" + p[4][4:]
    sink_name = "sink" + p[7][4:]
    
    
    if p[3] in module["conn_dict"]:
        module["conn_dict"][p[3]].update({port_name: sink_name}) 
    else:
        module["conn_dict"][p[3]] = {port_name: sink_name}
    
    print("p_connect_module_imput")
    #node ID(p[5]) inport = module input    

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc(debug=True)


#Reconocer archivo de entrada .afw como input
yacc.parse(data)
