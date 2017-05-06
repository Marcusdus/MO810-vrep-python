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
Start V-REP and load the scene: scenes/p3dx.ttt. 
```bash
# You need to define where the V-REP remoteApi dynamic library is. If the library is under a usual path, then you don't need to worry. 
# Otherwise set the path with LD_LIBRARY_PATH.
# If you are not sure of the paths, you can debug with strace (strace -eopen)

# To execute the walking algorithm and the graph
LD_LIBRARY_PATH=./ andabb

# To execute only the graph
LD_LIBRARY_PATH=./ andabb-graph

```

### Unit tests
To run all the unit tests
```bash
cd projetobb/
python -m unittest discover
```