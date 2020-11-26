# simLekuri
TIES481 Simulation assignment

## Code location

### Java version
`java_project/src/surgery/`

### python version
`Python_project/`

## How to run
### Java version
0. Get java
https://www.oracle.com/java/technologies/javase-jdk15-downloads.html

1. clone the repo\
`git clone https://github.com/RiskyRisto/simLekuri.git`

2. install javasim using intructions at:\
https://github.com/nmcl/JavaSim \
Maven generates a jar file containing the library

3. compile the source.\
If you are on mac you have to probably replace the ; with :\
`javac -cp ".;path/to/javasim-2.3.jar" -d bin src/surgery/*`

4. running the code \
`cd bin` \
`java -cp ".;path/to/javasim-2.3.jar" surgery.Main`

### Python version
0. get python
https://www.python.org/downloads/

1. clone the repo \
`git clone https://github.com/RiskyRisto/simLekuri.git`

2. Install libraries 
2.1. install simpy using instruction at
https://simpy.readthedocs.io/en/latest/simpy_intro/installation.html
2.2. install numpy using instruction at https://numpy.org/install/

3. run python script \
`python main.py`
