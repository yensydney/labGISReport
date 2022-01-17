# labGIS
## Purpose
The purpose of this project is to read a folder of historical map files, including shx, shp, qpj, prj, jpg, dbf, and cpg files. The code sorts the contents of
each file according to the phrase.
The output is each historical map file and their successful parsing, with any errors printed as well.
Then, the code exports a new json file for each of the map files, in the format of a dictionary. The dictionary for each file contains the records in order of 
their id, then in the order of their text within the phrase, and also the shape vertices. 
## Usage
Before anything, the user should make sure the pyshp extension is installed. An example of this is the pass:
export PYTHONPATH=/Users/yensydney/Desktop/lab/labthings/pyshp-2.1.3
After this, the user can run the code with their desired folder , i.e. python3 newMain.py /Users/yensydney/Desktop/lab/historical-map-groundtruth-25/
