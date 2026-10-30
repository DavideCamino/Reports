python run_exps.py --gates not_and.json --output not_and_sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_and.json --output not_and_qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_and.json --output not_and_oa.csv --penalties gate_penalties.json --solver qaoa --samples 65536 --num_restart 20 --n_experiments 30 --max_workers 16 

python run_exps.py --gates not_or.json --output not_or_sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_or.json --output not_or_qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_or.json --output not_or_oa.csv --penalties gate_penalties.json --solver qaoa --samples 65536 --num_restart 20 --n_experiments 30 --max_workers 16

python run_exps.py --gates toffoli.json --output toffoli_sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates toffoli.json --output toffoli_qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates toffoli.json --output toffoli_oa.csv --penalties gate_penalties.json --solver qaoa --samples 65536 --num_restart 20 --n_experiments 30 --max_workers 16 


python run_exps.py --gates not_and.json --output not_and_ancillary_sa.csv --penalties and_ancillary.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_and.json --output not_and_ancillary_qa.csv --penalties and_ancillary.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16; \
python run_exps.py --gates not_and.json --output not_and_ancillary_oa.csv --penalties and_ancillary.json --solver qaoa --samples 65536 --num_restart 20 --n_experiments 30 --max_workers 16