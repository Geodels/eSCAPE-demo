## Usage

Either via _jupyter notebooks_ or _python_ files.

```bash
python run_eSCAPE.py -i input.yml -v
```

where the `run_eSCAPE.py` script takes one required argument the input filename and an optional verbose command (`-v`).  To run the script in parallel simply use the `mpirun` command. As an example with N processors it will look like:

```bash
mpirun -np N python run_eSCAPE.py -i input.yml
```

`run_eSCAPE.py` consists of a limited number of calls to **eSCAPE**

```python
import eSCAPE
model = eSCAPE.LandscapeEvolutionModel(***)
model.runProcesses()
model.destroy()
```

as shown below:

```python
import argparse
import eSCAPE as sim

# Parsing command line arguments
parser = argparse.ArgumentParser(description='This is a simple entry to run eSCAPE model.',add_help=True)
parser.add_argument('-i','--input', help='Input file name (YAML file)',required=True)
parser.add_argument('-v','--verbose',help='True/false option for verbose', required=False,action="store_true",default=False)
parser.add_argument('-l','--log',help='True/false option for PETSC log', required=False,action="store_true",default=False)

args = parser.parse_args()
if args.verbose:
  print("Input file: {}".format(args.input))
  print(" Verbose is on? {}".format(args.verbose))
  print(" PETSC log is on? {}".format(args.log))

# Reading input file
model = sim.LandscapeEvolutionModel(args.input,args.verbose,args.log)

# Running model
model.runProcesses()

# Cleaning model
model.destroy()
```

## Input file

Input files for **eSCAPE** are based on [YAML](https://circleci.com/blog/what-is-yaml-a-beginner-s-guide/) syntax.

A typical file will look like this:

```YAML
name: Description of the what is going to be done in this simulation...

domain:
    filename: ['data/inputfileparameters.vtu','Z']
    flowdir: 1

time:
    start: 0.
    end: 1000000.
    tout: 1000.
    dt: 100.

sea:
    position: 0.
    curve: 'data/sealevel.csv'

climate:
    - start: 0.
      uniform: 1.0
    - start: 500000.
      map: ['data/inputfileparameters.vtu','R']
    - start: 500000.
      uniform: 2.0

tectonic:
    - start: 0.
      map: ['data/inputfileparameters.vtu','T1']
    - start: 100000.
      uniform: 0.
    - start: 50000.
      map: ['data/inputfileparameters.vtu','T2']

spl:
    m: 0.5
    n: 1.0
    Ke: 1.e-5

diffusion:
    hillslopeK: 5.e-2
    streamK: 300.
    oceanK: 100.
    maxIT: 2000

output:
    dir: 'outputDir'
    makedir: False

```

## Examples...


### 1- Synthetic model

<div align="center">
<img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/escape_mountain.gif" width="600"/>
</div>

+ repo - `mountain`

***

### 2- Regional model

<div align="center">
<img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/depo_ero.gif" width="800"/>
</div>

+ repo - `bluemountains`

***

### 3- Continental model

<div align="center">
<img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/depo_ero.gif" width="800"/>
</div>

+ repo - `australia`

***

### 4- Global model

<div align="center">
    <img width=1000 src="https://github.com/Geodels/eSCAPE/blob/master/images/FA.png" alt="eSCAPE" title="eSCAPE model"</img>
</div>

+ repo - `earth`

***
