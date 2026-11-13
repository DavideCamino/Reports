module circuit (
    input  wire A,
    input  wire B,
    input  wire C,
    output wire Y
);

    assign Y = C & ~(A | B);

endmodule
