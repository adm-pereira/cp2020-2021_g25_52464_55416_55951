# Simplified simulation of high-energy particle storms

### EduHPC 2018: Peachy assignment

(c) 2018 Arturo Gonzalez-Escribano, Eduardo Rodriguez-Gutiez
Group Trasgo, Universidad de Valladolid (Spain)

--------------------------------------------------------------

This is a version of the assignment customized by [João Lourenço](https://docentes.fct.unl.pt/joao-lourenco),
to be used in the course  of Concurrency and Parallelism at [FCT-NOVA](www.di.fct.unl.pt), 
edition 2020-21.

After João Lourenço customizations, the project was changed by Pedro Madeira, António Pereira and Diogo Lages.

--------------------------------------------------------------

# How to run the program

1. Open the Src directory in a linux terminal
2. `make all` or `make debug_all` if you want normal run or debug run, respectively
3. `./energy_storms_seq <array_size> <{name of all test files you want separated by an empty space}>` for sequential version
4. `./energy_storms_omp <array_size> <{name of all test files you want separated by an empty space}>` for parallel version

# How to run the program as we ourselves tested
(You need to have python3 installed as well as numpy, progress and matplotlib libraries)

This will run all tests given by the teacher and check if the output is correct as well for tests 01, 02 and 09.

1. `python3 scripts/run-tests.py test_files/tests.ini experiment_01 -d`. This will create .csv files in Src/logs/experiment_01
2. If you want to generate automatic plots run `python3 scripts/gen-plot.py`. This will generate plot pictures in Src/plots/experiment_01
3. Additionaly, you can also run experiment_02 and experiment_03 which are more specific tests we made.
