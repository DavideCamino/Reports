
(* techmap_celltype = "$_AND_" *)
module map_and(input A, B, output Y);
    TOFFOLI t (
        .A(A), .B(B), .C(1'b0),
        .P(), .Q(), .R(Y)
    );
endmodule

(* techmap_celltype = "$_XOR_" *)
module map_xor(input A, B, output Y);
    TOFFOLI t (
        .A(A), .B(1'b1), .C(B),
        .P(), .Q(), .R(Y)
    );
endmodule

(* techmap_celltype = "$_NOT_" *)
module map_not(input A, output Y);
    TOFFOLI t (
        .A(A), .B(1'b1), .C(1'b1),
        .P(), .Q(), .R(Y)
    );
endmodule
