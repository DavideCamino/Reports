import json
from enum import Enum
from pathlib import Path
import qubovert


DEFAULT_CONVERSION_TABLE = "gate_penalties.json"

class GateType(str, Enum):
    AND     = 'AND'
    OR      = 'OR'
    NOT     = 'NOT'
    XOR     = 'XOR'
    NAND    = 'NAND'
    NOR    = 'NOR'
    TOFFOLI = 'TOFFOLI'


class Gate:
    gate_type : GateType
    wires : list[str]

    def __init__(
                self,
                gate_type: GateType,
                wires: list[str]
            ) -> None:
        self.gate_type = gate_type
        self.wires = wires

class Circuit:
    gates : list[Gate]

    def __init__(
                self,
                gates: list[Gate]
            ) -> None:
        self.gates = gates

    def to_quso(self, conversion_table: str = DEFAULT_CONVERSION_TABLE, pin : dict | None = None) -> qubovert.QUSO:
        new_vars = 1
        q = qubovert.QUSO()
        with open(conversion_table) as f:
            ct = json.load(f)
        for gate in self.gates:
            matrix = ct[gate.gate_type]

            wires = gate.wires.copy()
            for i in range(len(matrix) - len(wires)):
                wires.append("__" + str(new_vars))
                new_vars += 1

            for i in range(len(matrix)):
                q[(wires[i], )] += matrix[i][i]

            for i in range(len(matrix)):
                for j in range(i+1, len(matrix)):
                    q[(wires[i], wires[j])] += matrix[i][j]

            

        q_const = q.subvalue({"1'b0": -1, "1'b1": 1})
        if pin is not None:
            return q_const.subvalue(pin)
        return q_const

    @classmethod
    def from_json(cls, file_name : str) -> "Circuit":
        """Load a circuit from the gate list written by extract.py."""
        with open(file_name) as f:
            data = json.load(f)

        gates = [
            Gate(GateType(gate["type"]), gate["vars"])
            for gate in data["gates"]
        ]
        return cls(gates)

    def get_wires(self) -> list[str]:
        wires = set()
        for gate in self.gates:
            for wire in gate.wires:
                wires.add(wire)

        return list(wires)
