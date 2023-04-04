# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 18:51:10 2023

@author: enriq
"""
import pprint
import json
import re

import axiParser

# =============================================================================
# TO DO:
    #Dividir el archivo en secciones -- OK
    #Elementos fuera de las secciones que siempre estan (reset replicator...) -- OK
    #Estandarizar la creacion de aristas -- OK
    #Estandarizar la creacion de nodos (sin buscar el modulo que debemos importar) -- OK
        #Completar el diccionario de nodo con las conexiones a cada puerto -- Not need, resueto
        #Crear el nodo con las conexiones necesarias -- Faltann sink y source
    
  
    #Lo podemos hacer en escritura sucesiva sobre el archivo con append, o creando
    #un gran """data""" y volcarlo entero sobre el arcvhivo

# =============================================================================
    
# =============================================================================
#  DUDAS:
    
    #Lo podemos hacer en escritura sucesiva sobre el archivo con append, o creando
    #un gran """data""" y volcarlo entero sobre el arcvhivo
    
    #Orden de funciones: importa solo el orden de llamada? Alguna regla de buen uso?
    
    #Widht de las señales: alguna vez van a ser de una anchura distinta
    # a la definida en DATA_WIDTH ??
    
    #Como organizar los archivos internos? Work? Crear directorios? 
    # --> Tener claro la organizacion de archivos y directorios en el proyecto final
    
    # Estoy cogiendo los puertos en orden, si hay uno no tiene numero y si hay mas
    # van desde el 0 al que toque. Tiene sentido esto? Y si se quiere dejar un puerto sin conectar?
    # Problema: si cojo como nombre los numeros que nos dan de entrada
        # 1. Exijo mucho más conocimiento al desarrollador de como es cada nodo por dentro
        # 2. Hay un porblema con el estandar actual donde si solo hay un puerto no se asigna numero
        # También habría que reordenar las entradas en los modulos para que sean todas 
        # iguales: data, valid, ready, last (futuro user)
# =============================================================================

# =============================================================================
# Library work?
# =============================================================================

module = {}
#Deberia poder coger cualquier archivo .afw usando regex
module = axiParser.axiFW_parse("axifw_InFile_2_0.afw") 


module_name = module["name"].upper()
pretty = json.dumps(module, indent=4)
print(pretty)



# =============================================================================
# FUNCIONES FAILITAR LA ESCRITURA EN LOS DISTINTOS APARTADOS
# =============================================================================
 
# Para que escriba todos los puertos axi_imput data, valid, ready, last
def print_module_input_ports(num):
    
    if num < 0:
        port_id = "input"
    else:
        port_id = "input_" + num.__str__()
    
    axi_port = """
    """ + '\t' + port_id + """_data        : in std_logic_vector(DATA_WIDTH -1 downto 0);
    """ + '\t' + port_id + """_valid       : in std_logic;
    """ + '\t' + port_id + """_ready       : out std_logic;
    """ + '\t' + port_id + """_last        : in std_logic;
    """
    return axi_port

# Para que escriba todos los puertos axi_output data, valid, ready, last
def print_module_output_ports(num):
    
    if num < 0:
        port_id = "output"
    else:
        port_id = "output_" + num.__str__()
    
    axi_port = """
    """ + '\t' + port_id + """_data        : out std_logic_vector(DATA_WIDTH -1 downto 0);
    """ + '\t' + port_id + """_valid       : out std_logic;
    """ + '\t' + port_id + """_ready       : in std_logic;
    """ + '\t' + port_id + """_last        : out std_logic;
    """
    return axi_port

#Para imprimir todas las señales (edges)
#De momento tomo DATA_WIDTH e ignoro la anchura
def print_signals():
    
    data_width = module["width"]
    edges = module["edges"]
    signals = ""
    edge_signals = ""
    
    #Itera directamente sobre keys
    for edge in edges:
        
        edge_signals = """\t--axi signals for """ + edge + """:
    """ + "signal " + edge + """_data    : std_logic_vector (DATA_WIDTH -1 downto 0);
    """ + "signal " + edge + """_valid   : std_logic;
    """ + "signal " + edge + """_ready   : std_logic;
    """ + "signal " + edge + """_last    : std_logic;\n\n"""
        
        signals += edge_signals
    
    #Extra signals: inner reset y alguna posible mas
    extra_signals = """\t--extra signals: 
    signal inner_reset    : std_logic;\n\n"""
    
    signals += extra_signals
        
    return signals

# Ipriir puertos en nun nodo: Queda sink/source
def print_node_input_ports(num, port, edge):
    
    if num < 0:
        port_id = "input"
    else:
        port_id = "input_" + num.__str__()
    
    axi_port = """
            """ + port_id + """_data => """ + edge + """_data,
            """ + port_id + """_valid => """ + edge + """_valid,
            """ + port_id + """_ready => """ + edge + """_ready,
            """ + port_id + """_last => """ + edge + """_last,""" 
    return axi_port


def print_node_output_ports(num, port, edge):
    
    if num < 0:
        port_id = "output"
    
    else:
        port_id = "output_" + num.__str__()
    
    axi_port = """
            """ + port_id + """_data => """ + edge + """_data,
            """ + port_id + """_valid => """ + edge + """_valid,
            """ + port_id + """_ready => """ + edge + """_ready,
            """ + port_id + """_last => """ + edge + """_last,""" 
    return axi_port

#Revisar esta funcion, está bastante sucia
def print_node(nodeID):
    
    str_node = """"""
    node = module["nodes"][nodeID]
    axi_module = node["node_type"].upper()
    
    str_node = """
    """ + nodeID + ": entity work." + axi_module +  """
        port map (
            clk => clk,
            rst => inner_reset,"""
    
    node_ports = module["connexions"][nodeID]
    ordered_ports = dict(sorted(node_ports.items()))
    
    in_ports = 0
    out_ports = 0
    for port, edge in ordered_ports.items():

        if re.match(r'in.*', port):
            in_ports += 1
        else:
            out_ports += 1
         
    in_port_num = 0
    out_port_num = 0
    for port, edge in ordered_ports.items():
        
        if re.match(r'in.*', port):
            if in_ports == 1:
                str_node += print_node_input_ports(-1, port, edge)
            else:
                str_node += print_node_input_ports(in_port_num, port, edge)
                in_port_num += 1
        else:
            if out_ports == 1:
                str_node += print_node_output_ports(-1, port, edge)
            else:
                str_node += print_node_output_ports(out_port_num, port, edge)
                out_port_num += 1
    
    
    str_node = str_node.rstrip(str_node[-1]) #para elimminar la ultima coma
    str_node += """
        );\n"""
    
    
    
    return str_node
    

def print_components():
    
    components = ""
    
    nodes = module["nodes"]
    
    for node in nodes:
        
        components+= print_node(node)
    
    return components


# =============================================================================
# FUNCIONES QUE CREAN LAS DIFERENTES PARTES DEL ARCHIVO VHD
# =============================================================================

# 1. Commented info and libraries
def print_intro():
    info = """
    ---------------------------------------------------------------------------
    -- File Generated via axiFw
    -- Autor: Enrique Ruiz Santos
    -- TFG
    -- VER 1.0
    -- Fecha: 27/03/2023
    --
    ---------------------------------------------------------------------------
    """
    libraries = """
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;\n\n"""
    intro = info + libraries
    return intro

# 2. Entity definition: Generic and Ports
def print_mod_entity():
    
    entity = "\nentity " + module_name + " is"
    
    # Posbilidad de mas parametros o de que no sea integer
    
    module_width = module["width"]
    generic = """\n
    Generic (
        DATA_WIDTH        : integer := """ + module_width.__str__() + """
    );"""
   
    num_input = module["input"]
   
    port = """
    Port (
        clk, rst        : in std_logic;
        
        --input axi ports"""
    if num_input == 1:
        port = port + print_module_input_ports(-1) 
    else:
        for i in range(0, num_input):
            port = port + print_module_input_ports(i)
   
    num_output = module["output"]         
    port +=  """
        --output axi ports"""
    if num_output == 1:
        port = port + print_module_output_ports(-1) 
    else:
        for i in range(0, num_output):
             port = port + print_module_output_ports(i)
     
    port += ");\n"
    
    end = "\nend " + module_name + ";\n\n"
    
    mod_entity = entity +generic + port + end
    return mod_entity

#3. Architecure: signal (edges) and components (nodes) and its connections 
def print_architecture():

    architecture = """""" 

    intro = "\narchitecture Behavioral of "   + module_name + " is\n\n"
    
    signals = print_signals()
    
    begin = """begin\n\n"""
    
    reset_rep = """\treset_replicator: entity work.reset_replicator
		port map (
			clk => clk, rst => rst,
			rst_out => inner_reset
		);\n\n"""

    components = print_components()
    
    end = "\n end Behavioral;"
       

    architecture = intro + signals + begin + reset_rep + components + end
    return architecture




# =============================================================================
# Main funcionality
# =============================================================================

data = print_intro() + print_mod_entity() + print_architecture()
file_name = module_name + ".vhd"

def create_file(content):
    f = open(file_name, "w")
    f.write(content)
    f.close()

create_file(data)



