import argparse
import eSCAPE as sim
from petsc4py import PETSc
MPIrank = PETSc.COMM_WORLD.Get_rank()

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

# Test values
EDmax = model.cumED.max()[1]
EDmin = model.cumED.min()[1]
hmax = model.hGlobal.max()[1]
hmin = model.hGlobal.min()[1]

if MPIrank == 0:
    EDmaxInstall = 8.4144388862
    EDminInstall = -1.08636116119
    hmaxInstall = 1264.82966136
    hminInstall = 19.2141465268
    print
    print('-------------------------------------------------------------')
    print('                 Testing eSCAPE installation                 ')
    print('-------------------------------------------------------------')
    print
    str_fmt = "{:35} {:9}"
    print(str_fmt.format('Maximum deposition thickness (m):', EDmax))
    print(str_fmt.format('Minimum deposition thickness (m):', EDmin))
    print
    print(str_fmt.format('Maximum elevation (m):', hmax))
    print(str_fmt.format('Minimum elevation (m):', hmin))
    print
    print('-------------------------------------------------------------')
    print('           Comparison with expected installation             ')
    print('-------------------------------------------------------------')
    print
    str_fmt = "{:35} {:5.2f}"
    print(str_fmt.format('Difference in max deposition thickness (m):', abs(EDmax-EDmaxInstall)))
    print(str_fmt.format('Difference in min deposition thickness (m):', abs(EDmin-EDminInstall)))
    print
    print(str_fmt.format('Difference in maximum elevation (m):', abs(hmax-hmaxInstall)))
    print(str_fmt.format('Difference in minimum elevation (m):', abs(hmin-hminInstall)))
    print
    print
    print('-------------------------------------------------------------')
    print('                      ending eSCAPE test                     ')
    print('-------------------------------------------------------------')

# Cleaning model
model.destroy()
