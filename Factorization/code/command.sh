python run_exps.py --gates mult_all.json --output mult_all-sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'; \
python run_exps.py --gates mult_all.json --output mult_all-qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'

python run_exps.py --gates mult_and.json --output mult_and-sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'; \
python run_exps.py --gates mult_and.json --output mult_and-qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'

python run_exps.py --gates mult_and_or.json --output mult_and_or-sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'; \
python run_exps.py --gates mult_and_or.json --output mult_and_or-qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'

python run_exps.py --gates mult_and_or_nand_nor.json --output mult_and_or_nand_nor-sa.csv --penalties gate_penalties.json --solver annealing --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'; \
python run_exps.py --gates mult_and_or_nand_nor.json --output mult_and_or_nand_nor-qa.csv --penalties gate_penalties.json --solver path-integral --samples 65536 --n_experiments 30 --max_workers 16 --pins '{"Mul[5]":1,"Mul[4]":-1,"Mul[3]":-1,"Mul[2]":-1,"Mul[1]":1,"Mul[0]":1}'
