
    ---------------------------------------------------------------------------
    -- File Generated via axiFw
    -- Autor: Enrique Ruiz Santos
    -- TFG
    -- VER 1.0
    -- Fecha: 27/03/2023
    --
    ---------------------------------------------------------------------------
    
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity AXIS_ACC_SQUARES is

    Generic (
        DATA_WIDTH        : integer := 32
    );
    Port (
        clk, rst        : in std_logic;
        
        --input axi ports
    	input_data        : in std_logic_vector(DATA_WIDTH -1 downto 0);
    	input_valid       : in std_logic;
    	input_ready       : out std_logic;
    	input_last        : in std_logic;
    
        --output axi ports
    	output_data        : out std_logic_vector(DATA_WIDTH -1 downto 0);
    	output_valid       : out std_logic;
    	output_ready       : in std_logic;
    	output_last        : out std_logic;
    );

end AXIS_ACC_SQUARES;


architecture Behavioral of AXIS_ACC_SQUARES is

	--axi signals for aristaA:
    signal aristaA_data    : std_logic_vector (DATA_WIDTH -1 downto 0);
    signal aristaA_valid   : std_logic;
    signal aristaA_ready   : std_logic;
    signal aristaA_last    : std_logic;

	--axi signals for aristaB:
    signal aristaB_data    : std_logic_vector (DATA_WIDTH -1 downto 0);
    signal aristaB_valid   : std_logic;
    signal aristaB_ready   : std_logic;
    signal aristaB_last    : std_logic;

	--axi signals for aristaC:
    signal aristaC_data    : std_logic_vector (DATA_WIDTH -1 downto 0);
    signal aristaC_valid   : std_logic;
    signal aristaC_ready   : std_logic;
    signal aristaC_last    : std_logic;

	--extra signals: 
    signal inner_reset    : std_logic;

begin

	reset_replicator: entity work.reset_replicator
		port map (
			clk => clk, rst => rst,
			rst_out => inner_reset
		);


    split: entity work.AXIS_SPLITTER_2
        port map (
            clk => clk,
            rst => inner_reset,
            input_data => source_1_data,
            input_valid => source_1_valid,
            input_ready => source_1_ready,
            input_last => source_1_last,
            output_0_data => aristaA_data,
            output_0_valid => aristaA_valid,
            output_0_ready => aristaA_ready,
            output_0_last => aristaA_last,
            output_1_data => aristaB_data,
            output_1_valid => aristaB_valid,
            output_1_ready => aristaB_ready,
            output_1_last => aristaB_last
        );

    mult: entity work.AXIS_MULTIPLIER
        port map (
            clk => clk,
            rst => inner_reset,
            input_0_data => aristaA_data,
            input_0_valid => aristaA_valid,
            input_0_ready => aristaA_ready,
            input_0_last => aristaA_last,
            input_1_data => aristaB_data,
            input_1_valid => aristaB_valid,
            input_1_ready => aristaB_ready,
            input_1_last => aristaB_last,
            output_data => aristaC_data,
            output_valid => aristaC_valid,
            output_ready => aristaC_ready,
            output_last => aristaC_last
        );

    acc: entity work.AXIS_ACCUMULATOR
        port map (
            clk => clk,
            rst => inner_reset,
            input_data => aristaC_data,
            input_valid => aristaC_valid,
            input_ready => aristaC_ready,
            input_last => aristaC_last,
            output_data => sink_1_data,
            output_valid => sink_1_valid,
            output_ready => sink_1_ready,
            output_last => sink_1_last
        );

 end Behavioral;