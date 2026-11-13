import subprocess
import time

def gen_verilog(file_name, mult1, mult2, prod):
    prog_template = '''
    module sat (
        input  wire [{0}:0] A,
        input  wire [{1}:0] B,
        output wire [{2}:0] Mul
        );
    
        assign Mul = A * B;
    
    endmodule
                '''
    program =prog_template.format(mult1, mult2, prod)
    with open(file_name, 'w') as file:
        file.write(program)


for i in range(50):
    start = time.time()
    gen_verilog('sat.v', i+2, i+2, 2*(i+2)-1)
    out = subprocess.run(['python', 'extract.py', '--out', 'test.json'], capture_output=True)
    stop = time.time()
    print(i+2, int(out.stdout.split()[-1]), stop-start)