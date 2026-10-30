import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from itertools import product, repeat
from typing import Any

import pandas as pd
from matplotlib import pyplot as plt

from qubo_from_gates import Circuit
from oquops.problem import QuadraticProblem

COUNT_COLUMN = 'num_occurrences'

def filter_var(vars : list[str]) -> list[str]:
    new_vars = []
    for var in vars:
        if not ('_' in var):
            new_vars.append(var)
    new_vars.sort()
    return new_vars

def task(
        i: int, 
        solver: Any,
        problem: QuadraticProblem, 
        n: int,
        pins: dict[str, int], 
        options: dict,
        variables: list[str]
    ) -> pd.Series:
    solution = solver.solve(problem, **options)
    print(f'Experiment {i + 1}/{n}, time: {solution.execution_time}')
    return solution.dataframe.assign(**pins).groupby(variables)[COUNT_COLUMN].sum()


def run_experiments(
        problem: QuadraticProblem,
        pins: dict[str, int], 
        solver: Any,
        variables: list[str],
        n_experiments: int = 30, 
        max_worker: int = 1,
        solve_options: dict | None = None
    ) -> list[pd.Series]:
    with ProcessPoolExecutor(max_workers=max_worker) as executor:
        sols = executor.map(
            task, range(n_experiments), 
            repeat(solver),
            repeat(problem), 
            repeat(n_experiments),
            repeat(pins), 
            repeat(solve_options or {}),
            repeat(variables)
            )
    return list(sols)


def summarize_results(results: list[pd.Series], pins: dict[str, int], variables: list[str]) -> pd.DataFrame:
    # Include zero counts for every assignment consistent with the pins.
    domains = [[pins[v]] if v in pins else [-1, 1] for v in variables]
    index = pd.MultiIndex.from_tuples(product(*domains), names=variables)
    counts = pd.concat([r.reindex(index, fill_value=0) for r in results], axis=1)
    return pd.DataFrame({'mean': counts.mean(axis=1), 'std': counts.std(axis=1)})


def plot_results(summary: pd.DataFrame) -> None:
    _, ax = plt.subplots(figsize=(12, 6))
    positions = range(len(summary))
    ax.errorbar(positions, summary['mean'], yerr=summary['std'], fmt='o', capsize=5)
    ax.set_xticks(positions, [', '.join(map(str, a)) for a in summary.index], rotation=45, ha='right')
    ax.set(
        xlabel='Assignment (A, B, C, Y)',
        ylabel='Mean occurrence count ± standard deviation',
        title='Assignment counts across experiments')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def create_solver(name: str) -> Any:
    if name == 'qaoa':
        from oquops.solvers.variational.qaoa_qiskit_aer import Qiskit_Aer_QAOA
        return Qiskit_Aer_QAOA()
    if name == 'brute-force':
        from oquops.solvers.exact.bruteforce_qubovert import BruteForceSolver
        return BruteForceSolver()
    from oquops.solvers.annealing.annealing_ocean import AnnealOcean
    return AnnealOcean()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--gates', default='extracted.json')
    parser.add_argument('--penalties', default='gate_penalties.json')
    parser.add_argument('--pins', type=json.loads, default={'Y': 1})
    parser.add_argument('--solver', default='qaoa', help='qaoa, annealing, path-integral, or brute-force')
    for name, default in [('levels', 2), ('samples', 2048), ('num_restart', 20), ('n_experiments', 10), ('max_workers', 4)]:
        parser.add_argument(f'--{name}', type=int, default=default)
    parser.add_argument('--output')
    parser.add_argument('--plot', action='store_true')
    return parser.parse_args(argv)

def build_option(args: argparse.Namespace) -> dict:
    options = {}
    if args.solver == 'qaoa':
        options = dict(level=args.levels, sample_shots=args.samples, num_restart=args.num_restart)
    elif args.solver in ('annealing', 'path-integral'):
        options = dict(num_samples=args.samples)
        if args.solver == 'path-integral':
            from dwave.samplers import PathIntegralAnnealingSampler
            options['sampler'] = PathIntegralAnnealingSampler()
    return options


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    options = build_option(args)
    circuit = Circuit.from_json(args.gates)
    variables = filter_var(circuit.get_wires())
    problem = QuadraticProblem.from_qubovert_quso(circuit.to_quso(args.penalties, pin=args.pins))
    results = run_experiments(
        problem=problem, 
        pins=args.pins, 
        solver=create_solver(args.solver),
        variables=variables,
        n_experiments=args.n_experiments, 
        max_worker=args.max_workers, 
        solve_options=options
        )
    summary = summarize_results(results, args.pins, variables)
    print(summary)
    if args.output:
        summary.to_csv(args.output)
    if args.plot:
        plot_results(summary)


if __name__ == '__main__':
    main()
