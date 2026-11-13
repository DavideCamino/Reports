import os
import json
import subprocess
import argparse

def rename_var(var):
    if '_' in var:
        return var[var.rfind("_"):]

    return var

def rename_gate(gate):
    if "_" in gate:
        return gate[gate.find("_") + 1:gate.rfind("_")]
    return gate

def signal(bit, bit_names):
    if isinstance(bit, str):
        return f"1'b{bit}"
    return bit_names.get(bit, f"net_{bit}")

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='name of output file.')
    args = parser.parse_args(argv)
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    subprocess.run(['yosys', '-s', 'synth.ys'])

    with open("mapped.json") as f:
        data = json.load(f)

    module = data["modules"]["sat"]

    # Map Yosys bit IDs to readable variable names
    bit_names = {}

    # Include ports first, so their names take priority
    for collection in ("ports", "netnames"):
        for name, info in module.get(collection, {}).items():
            bits = info["bits"]
            for i, bit in enumerate(bits):
                if not isinstance(bit, int):
                    continue

                if len(bits) == 1:
                    label = name
                else:
                    label = f"{name}[{i + info.get('offset', 0)}]"

                bit_names.setdefault(bit, label)



    # Extract variables
    variables = [rename_var(var) for var in sorted(set(bit_names.values()))]

    # Extract gates
    gates = []

    for instance, cell in module["cells"].items():
        gate_type = cell["type"]
        connections = {
            port: [signal(bit, bit_names) for bit in bits]
            for port, bits in cell["connections"].items()
        }

        conn = [rename_var(item) for row in list(connections.values()) for item in row]

        gates.append({
            "type": rename_gate(gate_type),
            "vars": conn
        })


    print("VARIABLES:")
    print(variables)

    print("\nGATES:")
    for gate in gates:
        print(gate["type"], gate["vars"])

    # Save extracted data
    with open(args.out+'.json', "w") as f:
        json.dump({
            "variables": variables,
            "gates": gates
        }, f, indent=2 )

    os.rename('circ.svg', args.out+'.svg')

if __name__ == '__main__':
    main()
