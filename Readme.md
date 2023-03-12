# MESA GYRE SdB Asteroseismic Fitting Tool
The fitting tool uses sdb grids created by Ostrowski et al. 2022 </br>
https://ui.adsabs.harvard.edu/abs/2021MNRAS.503.4646O/abstract </br>

- The grids information is extracted from the main grid database to reduce the file size. <br>
- The module for extracting the grid is 'GridExtract.py' located in the same directory<br> 
- It is saved as a sdb_grid.zip file along with the notebook. <br>
- Please extract the 'sdb_grid.zip' to the same folder where the notbook is located.<br>
- It will create a folder 'sdb_grid' and has all necessary files with in to run the notebook'<br>
- The 'sdb_grid' directory contains all the folders of the etracted grids and 'sdb_grid_extract.csv' file.

<br>

The grid parameters are as follows.

Metalicity (z) => 0.005 to 0.035 </br>
Metalicity (Fe/H) = > -0.46 to +0.39 </br>
Initial Mass (Mi) => 1.0 to 1.8 </br>
Envelope Mass (Menv) => 0.00001 to 0.01 </br>
Central Helium (coreHe) => 0.1 to 0.9 </br>

## Install all dependencies
```! pip install bokeh```
```! pip install numpy```
```! pip install pandas```

## sdBMESAGYRE python class
This class has mainly four modules. <br>
* ```ExtractGrid``` to extract grid from the main sdB model grid from Ostrowski et al. 2022. It is not necessary to use this module since the grid is already extracted. (Not added in the class Obj for now)
* ```FitModels``` to fit the grid to observations
* ```CheckModels``` to check the fitted models with custom periods
* ```PlotModels``` to plot and visualize the filtered models with the observations.<br>
Load these module by running the cell below


## How to run each module
* The target parameters are filled in to python dictionary.
* Use a unique target name for each Target model (It will create an output folder with the name)
* Add the observed/expected temparature and surface gravity ranges.
* List the all the possible multiplet input periods for fitting in the PeriodList

## Creating class object and fitting Models
* ```TeffObs``` and ```TeffObsErr``` in kK
* ```Sigma``` : Observation error limit
* ```PeriodList``` : add all possible l1 multiplets to this list before the fitting.
* ```GYREPeriodRange``` : GYRE period min max range in seconds # The range of observed period to be taken from the GYRE models.
* ```FitModels``` will create a ```xxxxx_seismicfit.csv``` file in the out put folder, it has all the information about the fitting.


## Checking the models
* Use the ```CustomPeriod``` list to add and remove periods.
* Do not change PeriodList in the target object 
* Change the ```Sigma``` to change the observation error limit
* It will print out the top results up to 150% worst solutions. (150 % is by default)
* You can change worstness percentage by adding a parameter called ```HowBad``` in the object example : ```sdBMESAGYRE(HowBad=200)```  
* You could select the best solution range by adding this parameters to the object ```NModels```. for example : ```sdBMESAGYRE(NModels=5000)``` (1000 is default)
* We can display best models or their range of parameters by changing variables in the ```CheckModels``` module. 
    * To display best models in each cases you can use ```DisplayModel=True```. It's True by default.
    * To display only the parametrer ranges you can use ```DisplayModelRange=True```. It's True by default. 

# Visualize the filtered solutions and cases
* The ```PlotModels``` will make an html file located in the output folder containing the filtered results interactively plotted
* The plot has a main plot panel with the Teff and logg axis
* The best solutions from all models and observation constrained models are presented.

* The bottom panel has two tables, 
    * Table on the right has best solutions from all observations.
    * Table on the left has best solutions from Observation limited models.
    * You can sort them based on any column by clicking on the column header.

* The plots will highlight upon clicking on the cells on the table.
    * Red high lights are models from all the observations
    * Blue highlights are modles constrained by observation.
    * There is also a merit map for all the models.
    * The observations with Sigma limit is represented as a yellow rectangle
    * click hide each legends based on use.

* Use the ```CustomPeriod``` list to add and remove periods.
* Change the ```Sigma``` to change the observation error limit
* It will print out the top results up to 150% worst solutions. 
* You can change worstness the percentage by adding a parameter called ```HowBad``` in the object example : ```sdBMESAGYRE(HowBad=200)```  
* You could select the best solution range by adding this parameters to the object ```NModels```. for example : ```sdBMESAGYRE(NModels=5000)```
