# AndaBB

MO810/MC959 - 1s2017 - V-REP remote API Python project. 


## Install instructions

This project can be installed with pip. It needs python 3.5 

```bash
pip install projetobb/
```

### Using virtualenv
You can use virtualenv to create an isolated Python environment. This is great if you have Python 2.7 as default and wants to install a Python 3 project. 

```bash
mkdir py3
virtualenv -p python3 py3
source py3/bin/activate

# Install the package. The -e option is used for the development mode (all the changes in the project will cause the executable to reflect those). 
pip install -e projetobb/

```

## Execute 
Start V-REP and load one of the scenes in scene directory, like: scenes/p3dx.ttt. 
```bash
# You need to define where the V-REP remoteApi dynamic library is. If the library is under a usual path, then you don't need to worry. 
# Otherwise set the path with the envinronment variable LD_LIBRARY_PATH or VREP_LIB_PATH. 
# If you are not sure of the paths, you can debug with strace (strace -eopen)

# Example of usage
export VREP_LIB_PATH=/VREP/programming/remoteApiBindings/python/python

# To avoid collisions
pioneer --controller=avoid-obstacle

# To follow the right wall
pioneer --controller=wall-follow

# The program help
#usage: pioneer [-h] [--controller {avoid-obstacle,wall-follow}] [--odometry]
#               [--plot-odometry-vs-gt] [-v]
#
#Pi#oneer V-REP controller.
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --controller {avoid-obstacle,wall-follow}
#                        Controller to be used.
#  --odometry            Use odometry to calculate the robot pose.
#  --plot-odometry-vs-gt
#                        Plot odometry vs ground-truth. Please also set
#                        --odometry.
#  -v, --verbose         increase output verbosity


```

### Unit tests
To run all the unit tests
```bash
cd projetobb/
python -m unittest discover
```