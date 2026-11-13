module circuit (
    input  wire [2:0] A,
    input  wire [2:0] B,
    output wire [5:0] Mul
    );

    assign Mul = A * B;

endmodule
