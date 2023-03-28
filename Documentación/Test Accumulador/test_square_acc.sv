`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/17/2023 11:29:57 AM
// Design Name: 
// Module Name: test_square_acc
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module test_square_acc(
    );
    parameter INPUT_DATA_FILE="input_data.mif";
	parameter INPUT_LAST_FILE="input_last.mif";
	parameter OUTPUT_DATA_FILE="output_data.mif";
	parameter DATA_WIDTH=32;
	
	parameter PERIOD = 10;
	
	//señales de control
    reg clk;
    reg rst;
    reg enable_rw;
    //bus de entrada 
    wire[DATA_WIDTH-1:0] axis_in_data;
    wire axis_in_valid, axis_in_ready, axis_in_last;    
    //bus de salida
    wire[DATA_WIDTH-1:0] axis_out_data;
    wire axis_out_valid, axis_out_ready; //no necesito last para este test
    
    
    always #(PERIOD/2) clk = ~clk;
    
    initial begin
    	clk = 0;
		rst = 1;
		enable_rw = 0;
		#(PERIOD*2) //hold reset
		rst = 0;
		#(PERIOD) //start now
		enable_rw = 1;
		#(PERIOD*100000); //test for 100000 cycles
		$stop;
    end

	//lector del fichero de datos
	helper_axis_reader 
	   #(.DATA_WIDTH(DATA_WIDTH), .FILE_NAME(INPUT_DATA_FILE), .SKIP(0), .BINARY(0))
	input_data_reader
	   (
	       .clk(clk),
	       .rst(rst),
	       .enable(enable_rw),
	       .output_valid(axis_in_valid),
	       .output_data(axis_in_data),
	       .output_ready(axis_in_ready)
	   );
	//lector del fichero de last
	helper_axis_reader 
	   #(.DATA_WIDTH(1), .FILE_NAME(INPUT_LAST_FILE), .SKIP(0), .BINARY(0))
	input_last_reader
	   (
	       .clk(clk),
	       .rst(rst),
	       .enable(enable_rw),
	       //.output_valid(), //no conectado, usa el de DATA
	       .output_data(axis_in_last),
	       .output_ready(axis_in_ready)
	   );
	   
	   
    //Aquí va el módulo diseñado
    sumador_cuadrados
        #(.DATA_WIDTH(DATA_WIDTH)) //valores genéricos
    dut
        (
            .clk(clk),
            .rst(rst),
            .axis_in_data(axis_in_data),
            .axis_in_last(axis_in_last),
            .axis_in_ready(axis_in_ready),
            .axis_in_valid(axis_in_valid),
            .axis_out_data(axis_out_data),
            .axis_out_valid(axis_out_valid),
            .axis_out_ready(axis_out_ready)
        );
    //


    //lector del fichero de salida y comprobador
    helper_axis_checker
        #(.DATA_WIDTH(DATA_WIDTH), .FILE_NAME(OUTPUT_DATA_FILE), .SKIP(0))
    output_data_checker
        (
            .clk(clk),
            .rst(rst),
            .enable(enable_rw),
            .input_valid(axis_out_valid),
            .input_ready(axis_out_ready),
            .input_data(axis_out_data)
        );
endmodule
