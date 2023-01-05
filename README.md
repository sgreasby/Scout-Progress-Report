# Description
This repository constains a tool for for generating Scouts BSA progress reports.

The tool comes in the form of a windows executable or a python script. While I encourage all users to run the python version of the script so they can see what it is doing, I also realize many people may not have even heard of python. As a result, I have also generated a windows executable for those users.

See the [releases section](https://github.com/sgreasby/Scout-Progress-Report/releases/) for the most recent stable version of the tool.

# Requirements
Before using the tool, log into Scoutbook and export troop advancement data.
See "Optional Steps to Make Output More Visually Pleasing" section below for steps to make the output look even better.

## Windows Executable
No other requirements. Just download the .exe file.
## Python Script
The script has been written for python 3.11 and utilizes the pandas, psutil, dominate, and matplotlib modules.

Before running the script for the first time, ensure python 3.11 or later is installed on your computer and install the requried modules by typing the following from the command line:

`pip install pandas`  
`pip install psutil`  
`pip install dominate`  
`pip install matplotlib`  

# Usage

## Windows Executable
Drag the desired CSV file and drop it onto the progress.py icon. When the script executes, it will prompt the user for all optional arguments. See the definition of all arguements in the "Python Script" section below. The script will generate HTML files in an "output" folder where the .exe file is located.

## Python Script
The script can be launched from the command line or from Windows. The script will generate HTML files in an "output" folder where the script file is located.

To lanuch from windows drag the desired CSV file and drop it onto the progress.py icon. When the script executes, it will prompt the user for all optional arguments.

To launch from the command line type the following, where {} denotes optional portions and [] denotes portions to be specified by the user.

`python progress.py {--date=[MM/DD/YYYY]} {--cubs} {--clean} [scoutbook.csv]`

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
#### --clean
Indicates that the old output should be cleaned (i.e. deleted) before generating new output. If this is not specified then old files will be not be deleted, however newly generated files may overwrite the old files.

### Optional Steps to Make Output More Visually Pleasing
Defining your own CSS file will allow you to override the styles defined in the script and customize the look and layout of the progress reports.

If an "img" folder exists in the folder where the script/executable is located then that the img folder will be copied into the output folder and the generated reports will reference images found in that folder. The reports should still render properly even if those files are missing. Specific file names are expected. Those file names are:
 - **background.jpg:** Background image for all reports
 - **emblem_bobcat.jpg:** Bobcat rank emblem
 - **emblem_lion.jpg:** Lion rank emblem
 - **emblem_tiger.jpg:** Tiger rank emblem
 - **emblem_wolf.jpg:** Wolf rank emblem
 - **emblem_bear.jpg:** Bear rank emblem
 - **emblem_webelos.jpg:** Webelos rank emblem
 - **emblem_arrow_of_light.jpg:** Arrow of Light rank emblem
 - **emblem_scout.jpg:** Scout rank emblem
 - **emblem_tenderfoot.jpg:** Tenderfoot rank emblem
 - **emblem_second_class.jpg:** Second Class rank emblem
 - **emblem_first_class.jpg:** First Class rank emblem
 - **emblem_star_scout.jpg:** Star Scout rank emblem
 - **emblem_life_scout.jpg:** Life Scout rank emblem
 - **emblem_eagle.jpg:** Eagle Scout rank emblem

