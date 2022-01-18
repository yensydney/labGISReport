# labGIS
## Purpose
The purpose of this project is to convert shp files to json files. This code reads one or more map folders.  
A map folder should include at least a dbf and shp file.  
The code sorts the contents of each file according to the phrase.
The output is each map file and their successful parsing, with any errors printed as well. The errors it can handle are: 
- different keys
- records with empty fields
- out of order indexes
- phrases that are not grouped together.
Then, the code produces a new json file in an output/ folder for each of the map files. The json file has the same name as the map file.  
The json file is in the format of a dictionary. The dictionary for each file contains the records in order of their id, then in the order of their text within the phrase, and also the shape vertices. 
## Prerequisite
Before anything, the user should make sure the pyshp extension is installed.  
Pyshp can be found here: https://pypi.org/project/pyshp/#overview  
An example of this is the pass:
export the pyshp-2.1.3 (or a different version) to PYTHONPATH.  
## Usage
To run the code, the user can use a root folder or their desired map folder  
python3 shpParser.py [root folder of one/multiple map folder(s)]  
i.e. python3 shpParser.py historical-map-groundtruth-25/  
## Contact
For bug reports and/or questions, email Sydney at yensydney@gmail.com.
