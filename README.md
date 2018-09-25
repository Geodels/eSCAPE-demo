<div align="center">
    <img width=1000 src="https://github.com/Geodels/eSCAPE/blob/master/images/bg.jpg" alt="eSCAPE" title="eSCAPE Model"</img>
</div>

## Content

This repository contains a series of 4 examples to run **eSCAPE**. Along with the jupyter notebooks used to run the input files, there is also a series of notebooks (**MeshGen.ipynb**) required to create the initial unstructured grids (**vtk** binary files).

The mesh creation could be a complicated process and relies on a series of libraries:
+ [meshio](https://pypi.org/project/meshio/)
+ [gdal](https://www.gdal.org)
+ [pygmsh](https://pypi.org/project/pygmsh/)
+ [fillit](https://github.com/Geodels/fillit)
+ [stripy](https://pypi.org/project/stripy/0.1.2/)
+ [lavavu](https://github.com/OKaluza/LavaVu)

For a quick start, it is recommended to use the [**Geodels escape-docker**](https://hub.docker.com/u/geodels/) image that is shipped with all the required libraries, the code as well as the examples found here. You will need to set the Docker preferences based on the specific memory and CPUs available in your local machine. Also it is recommended to attached a [volume to the Kitematic image](https://kitematic.com/docs/managing-volumes/) to be able to visualise the model outputs locally.  

All the examples have been designed to run on a single machine and should be completed in less than an hour. They are here to illustrate the basic capability of **eSCAPE**.

The code parallelisation relies on [petsc4py](https://pypi.org/project/petsc4py/) and scalability tests are still on-going. For now on, we have seen some good performance up to 64 CPUs using a mesh with more than 6 millions vertices. Our goal is to be able to run models with more than 10 millions nodes and over several hundreds of CPUs.

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
name: Description of what is going to be done in this simulation...

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

The YAML structure is shown through indentation (one or more spaces) and sequence items are denoted by a dash. At the moment the following component are available:

+ `domain`: definition of the unstructured grid containing the vtk grid `filename` and the associated field (here called `Z`) as well as the flow direction method to be used `flowdir` that takes an integer value between 1 (for SFD) and 12 (for Dinf) and the boundary conditions (`bc`: 'flat', 'fixed' or 'slope')

+ `time`: the simulation time parameters defined by `start`, `end`, `tout` (the output interval) and `dt` (the internal time-step).

Follows the optional forcing conditions:

+ `sea`: the sea-level declaration with the relative sea-level `position` (m) and the sea-level `curve` which is a file containing 2 columns (time and sea-level position).

+ `climatic` & `tectonic` have the same structure with a sequence of events defined by a starting time (`start`) and either a constant value (`uniform`) or a `map`.

Then the parameters for the surface processes to simulate:

+ `spl`: for the _stream power law_ with a unique parameter `Ke` representing the The erodibility coefficient which is scale-dependent and its value depend on lithology and mean precipitation rate, channel width, flood frequency, channel hydraulics. It is worth noting that the coefficient _m_ and _n_ are fixed in this version and take the value 0.5 & 1 respectively.

+ `diffusion`: hillslope, stream and marine diffusion coefficients. `hillslopeK` sets the _simple creep_ transport law which states that transport rate depends linearly on topographic gradient. River transported sediment trapped in inland depressions or  internally draining basins are diffused using the coefficient (`streamK`). The marine sediment are transported based on a diffusion coefficient `oceanK`. The parameter `maxIT` specifies the maximum number of steps used for diffusing sediment during any given time interval `dt`.

Finally, you will need to specify the output folder:

+ `output`: with `dir` the directory name and the option `makedir` that gives the possible to delete any existing output folder with the same name (if set to False) or to create a new folder with the give `dir` name plus a number at the end (e.g. outputDir_1 if set to True)

## Perfomance

The diagram below illustrates the performance of **eSCAPE** on a mesh with 6M+ nodes.

<div align="center">
<img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/performance.jpg" width="800"/>
</div>

Distribution on deposited sediments in both the marine and land regions is dependent of the main rivers positions and is happening on specific locations (river mouths, depressions). As these locations are irregularly positioned on the simulated domain it creates unbalancing issues that arise and potentially decrease overall scalability of the model with increasing number of CPUs.

## Examples...

### 0- Test

This simple model is used to test your **eSCAPE** installation. It provides two comparisons related to:

+ the _expected values_ that you should obtained if your installation is successful
+ runtime for both _serial_ and _parallel_ simulations

This test should take less than 1 minute. An example on how to visualise **eSCAPE** outputs in [**Paraview**](https://www.paraview.org/download/) is also provided.

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
    <img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/aussie.gif" width="800"/>
</div>
<div align="center">
   <img src="https://github.com/Geodels/eSCAPE-demo/blob/master/images/aussie2.gif" width="600"/>
</div>

+ repo - `australia`

***

### 4- Global model

<div align="center">
    <img width=1000 src="https://github.com/Geodels/eSCAPE/blob/master/images/FA.png" alt="eSCAPE" title="eSCAPE model"</img>
</div>

+ repo - `earth`

***
