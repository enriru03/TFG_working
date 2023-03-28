`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/17/2023 12:25:36 PM
// Design Name: 
// Module Name: sumador_cuadrados
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


module sumador_cuadrados (	
    clk, rst, 
    axis_in_data, axis_in_last, axis_in_ready, axis_in_valid,
    axis_out_data, axis_out_valid, axis_out_ready
);
	parameter DATA_WIDTH=32;
	
	input clk;
	input rst;
	
	input[DATA_WIDTH-1:0] axis_in_data;
	input axis_in_last;
	input axis_in_valid;
	output axis_in_ready;
	
	output[DATA_WIDTH-1:0] axis_out_data;
	output axis_out_valid;
	input axis_out_ready;
	
	
	reg[DATA_WIDTH-1:0] accumulated_data;
	reg full;
	
	assign axis_out_data = accumulated_data; //el dato sale tal cual del acumulador
	
	assign axis_out_valid = full; //si tenemos un dato acumulado, indico que es válido
	assign axis_in_ready = ~full; //si no tengo dato acumulado, indicio que puedo recibir
	
	initial begin
	   full = 0;
	   accumulated_data = 0;
	end
	
	always @(posedge clk) begin
	   if (full && axis_out_ready == 1) begin
	       full = 0;
	       accumulated_data = 0;
	   end else if (!full && axis_in_valid == 1) begin
	       accumulated_data = accumulated_data + axis_in_data*axis_in_data;
	       if (axis_in_last == 1) begin
	           full = 1;
	       end
	   end
	end
endmodule
