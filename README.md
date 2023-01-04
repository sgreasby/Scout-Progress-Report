# Description
This repository constains a tool for for generating Scouts BSA progress reports.

The tool comes in the form of a windows executable or a python script. While I encourage all users to run the python version of the script so they can see what it is doing, I also realize many people may not have even heard of python. As a result, I have also generated a windows executable for those users.

See the [releases section](https://github.com/sgreasby/Scout-Progress-Report/releases/) for the most recent stable version of the tool.

# Requirements
## Windows Executable
None. Just download the .exe file.
## Python Script
The script has been written for python 3.11 and utilizes the pandas and psutil modules.

Before running the script for the first time, ensure python 3.11 or later is installed on your computer and install the requried modules by typing the following from the command line:

`pip install pandas`
`pip install psutil`
`pip install dominate`

# Usage

## Windows Executable
Drag the desired CSV file and drop it onto the progress.py icon. When the script executes, it will prompt the user for all optional arguments. See the definition of all arguements in the "Python Script" section below. The script will generate HTML files in an "output" folder where the .exe file is located.

## Python Script
The script can be launched from the command line or from Windows. The script will generate HTML files in an "output" folder where the script file is located.

To lanuch from windows drag the desired CSV file and drop it onto the progress.py icon. When the script executes, it will prompt the user for all optional arguments.

To launch from the command line type the following, where {} denotes optional portions and [] denotes portions to be specified by the user.

`python progress.py {--date=[MM/DD/YYYY]} {--cubs} [scoutbook.csv]`

### Required Arguments
#### [scoutbook.csv]
This outlines the path to the CSV file exported from Scoutbook.

### Optional Arguments
#### --date=[MM/DD/YYYY]
Defines the date of of the last progress report. All progress made since this date will be considered new.
If omitted, a default date of 1/1/1980 wil be used.
#### --css=[style.css]
Defines the CSS style sheet to customize the look of the progress reports.
If omitted, a default style will be applied.
#### --cubs
Indicates that the progress report is generated for Cub Scouts. When this flag is set, the script will not display progress towards eagle, and will indicate Cub Scout and Webelos specific advancement and awards.
If omitted, only Scouts BSA advancement and awards will be displayed.

### Optional Steps to Make Output More Visually Pleasing
Defining your own CSS file will allow you to override the styles defined in the script and customize the look and layout of the progress reports.

If an "img" folder exists in the folder where the script/executable is located then that the img folder will be copied into the output folder and the generated reports will reference images found in that folder. The reports should still render properly even if those files are missing. Specific file names are expected. Those file names are:
 - unitlogo.jpg: Background image for all reports
 - bobcat.jpg: Bobcat rank emblem
 - lion.jpg: Lion rank emblem
 - tiger.jpg: Tiger rank emblem
 - wolf.jpg: Wolf rank emblem
 - bear.jpg: Bear rank emblem
 - webelos.jpg: Webelos rank emblem
 - arrowoflight.jpg: Arrow of Light rank emblem
 - scout.jpg: Scout rank emblem
 - tenderfoot.jpg: Tenderfoot rank emblem
 - secondclass.jpg: Second Class rank emblem
 - firstclass.jpg: First Class rank emblem
 - star.jpg: Star Scout rank emblem
 - life.jpg: Life Scout rank emblem
 - eagle.jpg: Eagle Scout rank emblem

