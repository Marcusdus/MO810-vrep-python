# MO810-vrep-python

MO810/MC959 - 1s2017 - V-REP remote API Python project. 


## Install instructions

This project can be installed with `pip`. It needs python 3.5 

```bash
git clone https://github.com/luwood/MO810-vrep-python.git
pip install MO810-vrep-python/
```

**Windows users**: this project depends on Numpy and Scipy packages, 
you won't be able to just install them by using `pip`.
You can find the install instructions in the [SciPy page](https://www.scipy.org/install.html).
I've used the precompiled wheels provided by [Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs/).
In case you are not familiar with wheels, you just need to call `pip install` on them, like this:
```bash
# Example
pip install D:\Downloads\scipy-0.19.0-cp36-cp36m-win32.whl
```


### Using virtualenv
You can use virtualenv to create an isolated Python environment. This is great if you have Python 2.7 as default and wants to install a Python 3 project. 

```bash
mkdir py3
virtualenv -p python3 py3
source py3/bin/activate

# Install the package. The -e option is used for the development mode (all the changes in the project will cause the executable to reflect those). 
pip install -e  MO810-vrep-python/

```

## Execute 
Start V-REP and load one of the scenes in scene directory, like: scenes/p3dx.ttt.
 
**You will need to define where the V-REP remoteApi dynamic library is**.
You can do that setting the envinronment variable `VREP_LIB_PATH` (it also works on linux
if you set up `LD_LIBRARY_PATH`).
```bash
# Linux
export VREP_LIB_PATH=/VREP/programming/remoteApiBindings/lib/lib/64Bit

# Windows
set VREP_LIB_PATH="C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU\programming\remoteApiBindings\lib\lib\64Bit"
```

Now to execute the robot is simple:
```bash 
# To plot the localization calculated with odomotry and Kalmnan filters.
pioneer --kalman 1 --plot-odometry-vs-gt
# "--kalman 1" means the algorithm will use one base as a landmark.
# Use the scene p3dx-original-with-script-transceiver-3bases.ttt

# You can also start a HTTP server that will serve the robot current estimated pose
# on the address http://localhost:8090/pose
pioneer --kalman 3 --plot-odometry-vs-gt --server

# To avoid collisions
pioneer --controller=avoid-obstacle

# To follow the right wall
pioneer --controller=wall-follow

# You can check other options
pioneer --help
```

### Unit tests
To run all the unit tests
```bash
cd MO810-vrep-python/
python -m unittest discover
```

## REST API
This project also exposes a REST API to get the current pose of the robot under
`http://localhost:8090/pose`.

It will just return a string with the pose. Example:
```bash
# X                 Y                   Orientation(radians) Orientation(degrees)
-5.199949362545673, 2.3613965813855646, 0.21013562287192755, 12.039884315914179
```

