# Electronic_model_building
- The program is created to build a backend for electronic models.
- main.py: YOU can run this file to test basic functionality of this program.
```
python3 main.py
```
- Test flows:
Now you must guarantee you are in the current working directory. And then you can run these commands.
```
cd Test
python3 test_main.py
```
If you want to run specific single unit test, you can run the following commands.
```
cd Test/unit
python3 test_Math.py
```

- The program structure is displayed as follows：
## Data
The Data which contains the parameters for the model is stored in this directory, mainly including:
- Tower
- Span
- Cable
- Lump

These data will be initialized in the Dirver Directory. Now they are Excel tables which is friendly to look through. They will be replaced by XML files or Json files later which are suitable for reading when used by Web applications.

## Driver
This directory contains all the actions and flows of modeling and calculating.
- 1. Initialize the model by reading parameters from Data directory. (Input_Tower1.xlsx/Input_Cable1.xlsx/Input_Span1.xlsx/Lump.xlsx/...)
- 2. Update the model matrix by describing the flows of the modeling.(Tower/Cable/OHL/Lightning)
- 3. Merge the model matrix by predefined orders. (A/L/C/P/Z/R  -> H)
- 4. Calculate the specific parameters by model matrix.
This directory is just used to describe the actions of modeling and calculating, the modeling and calculating details are indicated in Function directory and Model directory.
## Function
### Calculators
We state all of the calculations in this directory.
- Capacitance.py : We will indicate all of functions which is used to calculate the capacitance of the model.(Tower/Cable/OHL)
- Impedance.py : We will indicate all of functions which is used to calculate the impedance of the model.(Tower/Cable/OHL)
- Inductance.py : We will indicate all of functions which is used to calculate the inductance of the model.(Tower/Cable/OHL)
### Builders
We state all of the building matrix or parameters in this directory.
- To be updated...
## Model
We state all of data structures which should be encapsulated to classes, by which it will be easy and friendly to extend functions and parameters.
### main
We state all of the main classes in this directory.
- Tower.py : we created a Tower class which describes the parameters and matrix which will be used in model construction.
- Cable.py : we created a Cable class in this file.
- OHL.py : ...
- Lightning.py : we created a Lightning class and a stroke class in this file. Lightning class contains much stroke object which can consist of the whole Lightning object.
- Lump.py : ...
### inferior
We state all of inferior classes in this directory which will not be used directly in Driver directory but will be used by main classes.
- Wires.py
- Node.py
- Constant.py
- Info.py
- Ground.py
- Device.py
## Test
We created a test engineering in this directory.
- test_main.py : we will dicover and run all of test cases by this python script.
### unit
- test_Model.py : we created many test cases to test Model initialization and Model calculation.
- test_Math.py : we created many test cases to test Math calculation in the Utils/Math.py directory.
### integration
Integration test will be added and updated after front-end is finished, which will be used to test whole flows of modeling and calculation.
- To be updated...
## Utils
- Math.py : we indicated all of the math functions here.
- Matrix.py : we indicated all of the basic matrix operations that we need here.
