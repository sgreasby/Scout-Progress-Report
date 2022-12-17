# Description
This repository constains a python script for generating Scouts BSA progress reports

# Requirements
The script has been written for python 3.11 and utilizes the pandas and psutil modules.

Before running the script for the first time, ensure python 3.11 or later is installed on your computer and install the requried modules by typing the following from the command line:

`pip install pandas`
`pip install psutil`

# Usage
The script can be launched from the command line or from Windows.

To lanuch from windows drag the desired CSV file and drop it onto the progress.py icon. When the script executes, it will prompt the user for all optional arguments.

To launch from the command line type the following, where {} denotes optional portions and [] denotes portions to be specified by the user.

`python progress.py {--date=[MM/DD/YYYY]} {--id=[scoutid]} {--cubs} [scoutbook.csv]`

## Required Arguments
### [scoutbook.csv]
This outlines the path to the CSV file exported from Scoutbook.


## Optional Arguments
### {--out=[outfile.txt]}
Specifies the file name where all output will be written.
If omitted, output will be displayed to the screen.
### --date=[MM/DD/YYYY]
Defines the date of of the last progress report. All progress made since this date will be considered new.
If omitted, a default date of 1/1/1980 wil be used.
### --id=[scoutid]
Tells the script to only generate a progress report for a specific scout.
If omitted, a progress report will be generated for all scouts listed in the CSV file.
### --cubs
Indicates that the progress report is generated for Cub Scouts. When this flag is set, the script will not display progress towards eagle, and will indicate Cub Scout and Webelos specific advancement and awards.
If omitted, only Scouts BSA advancement and awards will be displayed.
