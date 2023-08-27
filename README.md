# Sensor_Characterisation_Plateform
- Author: Yehya SHARIF
- Supervised by: Paul CHAILLOU

## Definition
This platform is designed to synchronize the displacement of 3D Printer with the sensor measurement,and evaluate the performance of the sensors by calculating characteristics such as the hysterisis,linearity, and plotting the calibration curves of sensors.

## Prerequisite
The necessary python librairies are: pynput, matplotlib, pyserial, numpy, pandas, itertools, statistics, and scipy.
```console
pip install pynput
pip install matplotlib
pip install pyserial
pip install numpy
pip install pandas
pip install scipy
```
## Installation


1. Install all the neccessary libraries.


2. Add the submodules by running the following command in the terminal:
```console
git submodule update --init --recursive
```

## Steps
To begin the characterization phase:
1. After adding all submodules, ensure that the correct serial port and baud rate are set in the 's Python file.

   For example, if i want to  ensure that the correct serial port and baud rate are set in `Main.py` file we can do the following stuff:
     1. See the port and the baud rate in the Arduino IDE.
     2. Check the compatibility of each one in the `Main.py` by modifying the following code in the `Main.py`:

```console 
testsensor=ts.Testing_Sensor_Pressure(port="/dev/ttyACM3",baud="9600")
Distance_Sensor = ds.Distance_Sensor(port="/dev/ttyACM2",baud="9600")
printer = CR10_test.SerialDuino(port="/dev/ttyUSB0",baud="9600")
```
(You should verify the port of the printer with the arduino IDE: "/dev/ttyUSB0")

2. After that, debug each sensor to verify that it returns the right values.
   For example, to confirm the correctness of the readings from the "hc-c1100-p" sensor, execute the following command in the terminal(the `main_test.py` is existing in each submodule existing in this git reposite):

```console
python3 main_test.py
```

3. Execute the `Main.py` file by adding the following command in the terminal:

```console
python3 Main.py
```
 and follow the orders provided by the code.

4. After the .csv file is generated, run the `Sensor_Characterisation.py` file, by putting the following command in the terminal:
```console
python3 Sensor_Characterisation.py
```
This step will generate the desired plots,and print the desired characteristics.
(You can specify the desired figures, and characteristics by modifying the code presented in the Sensor_Characterisation.py file) 

**Important**
If you want to add a new sensor, Add an intermediate .py file such as Distance_Sensor.py,between the original .py file (e.g., `HG_C1100_P.py`) and the Main.py file,you can initialise the sensor in the `Main.py` file lusing the following lines as an example for the `HG_C1100_P` sensor:
(Change the name of the imported folders to be compatible with the python language.For example: hc-c1100-p folder name into  the hc1100 folder name)
```console
   import Distance_Sensor as ds
   Distance_Sensor = ds.Distance_Sensor(port="/dev/ttyACM2",baud="9600")
```
You can change this code in order to initialise another sensor.
## Links
You can see the following link to see the 3D attachment pieces: https://gitlab.inria.fr/defrost/hardware/cao/attachment-pieces-3d-printer/-/tree/main/attachement_pieces_for_soft_waveguide_sensor
To use those pieces, you should put the begin position like 198mm (150mm+48mm) for 48 mm like initial lenght for the sensor
