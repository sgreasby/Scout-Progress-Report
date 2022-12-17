# Description
This repository constains a script for generating Scouts BSA progress reports

# Requirements
The script has been tested with python 3.11.

# Usage
python  {--date=[MM/DD/YYYY]} {--id=[scoutid]} {--cubs} [scoutbook.csv]

## Required Arguments
### [scoutbook.csv]
This outlines the path to the CSV file exported from Scoutbook.

## Optional Arguments
### --date=[MM/DD/YYYY]
This defines the date of of the last progress report. All progress made since this date will be considered new.
### --id=[scoutid]
This is used to tell the script to only generate a progress report for the indicated scout (rather than for all scouts).
### --cubs
This is used to indicate that the progress report is generated for Cub Scouts. When this flag is set, the script will not display progress towards eagle, and will indicate Cub Scout and Webelos specific advancement and awards. 

