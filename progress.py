#!/usr/bin/env python
###########################################################
"Scout Progress Report Generator"

__author__     = "Steven Greasby"
__copyright__  = "Copyright (C) 2022-2023 Steven Greasby"
__license__    = "GPL 2.0"
__url__        = "http://github.com/sgreasby/Scout-Progress-Report"
__maintainer__ = "Steven Greasby"
###########################################################
import os
import sys
import datetime
import re
import shutil
import webbrowser

# The following modules are required, tell non python users how to get them.
try:
    import pandas
except:
    print("type \"pip install pandas\" from the command line then try again") 
try:
    import psutil
except:
    print("type \"pip install psutil\" from the command line then try again") 
try:
    import dominate
    from dominate.tags import *
except:
    print("type \"pip install dominate\" from the command line then try again") 

# While not needed to run the script, autopytoexe is used to build .exe releases
    
# Figure out if user ran from command line or clicked icon 
windows= 1 if psutil.Process(os.getpid()).parent().name() == 'py.exe' else 0
# If launched via windows, the window may close before the error can be read
# If this happens, just set windows=1 and run from the command line to see error.
# Also set this to 1 when gnerating .exe file using auto-py-to-exe
#windows=1
# Debugging code
warnings=False

#pandas.set_option('display.max_rows', None)
#pandas.set_option('display.max_columns', None)

default_style = """
html,body,blockquote,code,h1,h2,h3,h4,h5,h6,p,pre{margin:0;padding:0}
button,fieldset,form,input,legend,textarea,select{margin:0;padding:0}
fieldset{border:0}
a,a *{cursor:pointer}
div{margin:0;padding:0;background-color:transparent;text-align:left}
hr,img{border:0}
applet,iframe,object{border:0;margin:0;padding:0}
button,input[type=button],input[type=image],input[type=reset],input[type=submit],label{cursor:pointer;}
ul,li{list-style:none;margin:0;padding:0;}
strong{font-weight:bold;}
em{font-style:italic;}


caption {
  width: 1px;
  font-weight: bold;
  text-align: left;
  white-space: nowrap;
  padding-left:20px;
}
th {
  width: 1px;
  font-weight: bold;
  text-align: left;
  white-space: nowrap;
  padding-left:20px;
}
td {
  width: 1px;
  text-align: left;
  white-space: nowrap;
  padding-left:20px;
}

.eagle_reqs {
  padding-left:20px;
}
.recent_progess {
  padding-left:20px;
}
.recent_rankups {
  padding-left:20px;
}
.approved_adventures {
  padding-left:20px;
}
.complete_adventures {
  padding-left:20px;
}
.approved_mbs {
  padding-left:20px;
}
.complete_mbs {
  padding-left:20px;
}
.approved_awards {
  padding-left:20px;
}
.requirement_progress {
  padding-left:20px;
}
.rank_progress {
  padding-left:20px;
}
.rank_progress p {
  padding-left:20px;
}
.adventure_progress {
  padding-left:20px;
}
.adventure_progress p {
  padding-left:20px;
}
.mb_progress {
  padding-left:20px;
}
.mb_progress p {
  padding-left:20px;
}
.award_progress {
  padding-left:20px;
}
.award_progress p {
  padding-left:20px;
}
.requirements {
  padding-left:20px;
}




body {
  background-image: url('img/unitlogo.jpg');
  background-size: auto;
  background-repeat: no-repeat;
}
.page {
  margin: 0px;
  height:100%;
  background: rgba(255, 255, 255, 0.8);
}
.name {
  display: inline-block;
}
.rank {
  display: inline-block;
}
.rank_logo {
  height: 30px;
  padding: 0px;
}
hr {
  border: 1px solid black;
  margin-left: 0px;
}

"""

eagle_mbs=[['Camping'],
           ['Citizenship in the Community'],
           ['Citizenship in the Nation'],
           ['Citizenship in the World'],
           ['Communication'],
           ['Cooking'],
           ['Cycling','Hiking','Swimming'],
           ['Emergency Preparedness','Lifesaving'],
           ['Environmental Science','Sustainability'],
           ['Family Life'],
           ['First Aid'],
           ['Personal Fitness'],
           ['Personal Management'],
           ['Citizenship in Society']]

rankfile = {'Bobcat'         : 'bobcat.jpg',
            'Lion'           : 'lion.jpg',
            'Tiger'          : 'tiger.jpg',
            'Wolf'           : 'wolf.jpg',
            'Bear'           : 'bear.jpg',
            'Webelos'        : 'webelos.jpg',
            'Arrow of Light' : 'arrowoflight.jpg',
            'Scout'          : 'scout.jpg',
            'Tenderfoot'     : 'tenderfoot.jpg',
            'Second Class'   : 'secondclass.jpg',
            'First Class'    : 'firstclass.jpg',
            'Star Scout'     : 'star.jpg',
            'Life Scout'     : 'life.jpg',
            'Eagle Scout'    : 'eagle.jpg'}

#TODO:Are these right?
cub_rank_reqs={'Bobcat'          :['1','2','3','4','5','6','7'],
               'Lion'            :['1a','1b','1c','1d','1e','2a','2b','2c'],
               'Tiger'           :['1a','1b','1c','1d','1e','1f','2'],
               'Wolf'            :['1a','1b','1c','1d','1e','1f'
                                   '2a','2b','2c','2d','2e','2f','2g','2h','2i',
                                   '3a','3b','4a','4b'],
               'Bear'            :['1a','1b','1c','1d','1e','1f'
                                   '2a','2b','2c','2d','2e','2f','2g','2h','2i',
                                   '3a','3b','4a','4b'],
               'Webelos'         :['1','2a','2b','2c','2d','2e',
                                   '3a','3b','3c','3d','3e','3f','3g','3h','3i','3j','3k','3k','3m','3n',
                                   '4a','4b','5a','5b'],
               'Arrow of Light'  :['1','2a','2b','2c','2d',
                                   '3a','3b','3c','3d','3e','3f','3g','3h','3i','3j','3k','3k','3m','3n',
                                   '4a','4b','5a','5b']}

bsa_rank_reqs={'Scout'          :['1a','1b','1c','1d','1e','1f',
                                  '2a','2b','2c','2d','3a','3b',
                                  '4a','4b','5','6','7'],
               'Tenderfoot'     :['1a','1b','1c','2a','2b','2c',
                                  '3a','3b','3c','3d',
                                  '4a','4b','4c','4d',
                                  '5a','5b','5c',
                                  '6a','6b','6c','7a','7b',
                                  '8','9','10','11'],
               'Second Class'   :['1a','1b','1c',
                                  '2a','2b','2c','2d','2e','2f','2g',
                                  '3a','3b','3c','3d',
                                  '4','5a','5b','5c','5d',
                                  '6a','6b','6c','6d','6e',
                                  '7a','7b','7c',
                                  '8a','8b','8c','8d','8e',
                                  '9a','9b','10','11','12'],
                'First Class'   :['1a','1b','2a','2b','2c','2d','2e',
                                  '3a','3b','3c','3d','4a','4b',
                                  '5a','5b','5c','5d',
                                  '6a','6b','6c','6d','6e',
                                  '7a','7b','7c','7d','7e','7f'
                                  '8a','8b','9a','9b','9c','9d',
                                  '10','11','12','13'],
               'Star Scout'     :['1','2','3','4','5','6','7','8'],
               'Life Scout'     :['1','2','3','4','5','6','7','8'],
               'Eagle Scout'    :['1','2','3','4','5','6','7']}


####################################
# Global Variables
####################################
scoutbook=pandas.DataFrame()
cols=pandas.DataFrame()
default_date=pandas.to_datetime(["1/1/1980"])[0]
last_review=default_date
cubs=False
stylesheet=None

####################################
# Functions
####################################
def warn(*args, **kwargs):
    if warnings:
        print("WARNING: ",end="")
        return print(*args, **kwargs)
    else:
        return True

def error(*args, **kwargs):
    print("ERROR: ",end="")
    return print(*args, **kwargs)

def usage():
    if windows:
        if scoutbook.empty:
            print("Drag CSV file on top of %s icon" %(sys.argv[0]))
        input("\nPress any key to continue...")
    else:
        print("Usage: %s {--date=[MM/DD/YYYY]} {--css=[style.css]} {--cubs} [scoutbook.csv]\n\n" %(sys.argv[0]))
    sys.exit()

def csv_open(csv_file):
    col_names=pandas.DataFrame()
    data=pandas.DataFrame()
    print("Opening %s" %(csv_file))
    try:
        # First row of CSV contains column names.
        # However some rows have an undocumnted column
        # Add dummy column to avoid errors when reading in data
        col_names = pandas.read_csv(csv_file, nrows=1,header=None).values.flatten().tolist()+['Undocumented']
    except:
        print("Failed to read %s." %(csv_file))
        usage()
    else:
        # read the rest of the CSV file
        # Skip first row (col names) and use names determined above
        data = pandas.read_csv(csv_file, skiprows=1,names=col_names)
    return data,col_names


def convert_date(date):
    try:
        # Use pandas to convert date to datetime object
        date=pandas.to_datetime([date])[0]
    except:
        error("%s does not appear to be a valid date."%date)
        usage()
    return date

def print_list(table_cls,table_caption,entries):
    with table(cls='%s %s'%('table table-striped',table_cls)):
        caption(table_caption)
        with tbody():
            if len(entries) == 0:
                with tr():
                    td("None")
            else:
                for entry in entries:
                    with tr():
                        td(entry)

def print_reqs(achievement,recent_reqs,previous_reqs,remaining_reqs):
    max_cols = max(len(recent_reqs),len(previous_reqs))
    if remaining_reqs:
        max_cols = max(max_cols,len(remaining_reqs))

    with table(cls='table table-striped requirements'):
        caption(achievement)                                
        with tbody():
            with tr():
                th("Recently Completed")
                if len(recent_reqs) >0:
                    for req in recent_reqs:
                        td(req)
                else:
                    td("None",colspan=max_cols)
            with tr():
                th("Previously Completed")
                if len(previous_reqs) >0:
                    for req in previous_reqs:
                        td(req)
                else:
                    td("None",colspan=max_cols)
            if remaining_reqs:
                with tr():
                    th("Remaining")
                    if len(remaining_reqs) >0:
                        for req in remaining_reqs:
                            td(req)
                    else:
                        td("None",colspan=max_cols)

if len(sys.argv)<2:
    usage()

if windows:
    scoutbook,cols=csv_open(sys.argv[1]);        

    response=input("Enter date of last progress report or leave blank for none (MM/DD/YYYY): ")
    if response:
        last_review=convert_date(response)

    response=input("Enter style sheet or leave blank for default styling: ")
    if response:
        stylesheet=response

    response='unknown'
    while not response in ['y','Y','n','N','']:
        response=input("Run script for Cub Scouts? y/N: ")

    if response in ['y','Y']:
        cubs=True

else:
    for arg in sys.argv[1:]:
        if arg.startswith('--date='):
            junk,value = arg.split('=')
            last_review=convert_date(value)
        elif arg.startswith('--css='):
            junk,value = arg.split('=')
            stylesheet=value
        elif arg == '--cubs':
            cubs=True
        elif not arg.startswith('--'):
            scoutbook,cols=csv_open(arg);        
        else:
            usage()

    if scoutbook.empty:
        usage()

#######################################
# Clean up imported data before using it
#######################################
# As of 2022-12-11, Scoutbook CSV files can have corruption starting with the MarkedCompletedBy column
# Those are not very useful so just drop them
drop_idx = cols.index('MarkedCompletedBy')
try:
    scoutbook.drop(cols[drop_idx:], axis=1,inplace=True)
    cols=cols[:drop_idx]
except:
    pass


# This script wont use Version or Middle Name columns so drop those as well
try:
    drop_idx = cols.index('Version')
    scoutbook.drop(cols.pop(drop_idx), axis=1,inplace=True)
    
    drop_idx = cols.index('Middle Name')
    scoutbook.drop(cols.pop(drop_idx), axis=1,inplace=True)
except:
    pass

# Drop duplicate lines
# This should only happen if two verions of a requirement were completed
scoutbook.drop_duplicates(keep='last',inplace=True)

# Drop any columns that only contain NaN
#for col in cols:
#    if scoutbook[col].isnull().values.sum()==scoutbook.shape[0]:
#        scoutbook.drop(col, axis=1,inplace=True)

scoutIDs=scoutbook['BSA Member ID'].unique()

#Convert all dates to datetime
scoutbook['Date Completed'] = pandas.to_datetime(scoutbook['Date Completed'])

print("")

outFiles=[]
import shutil
if os.path.isdir('output'):
    try:
        shutil.rmtree('output')
    except:
        error("Unable to delete output folder")
        exit()

os.mkdir('output')
if os.path.isdir('img'):
    shutil.copytree('img',os.path.join('output','img'))
os.chdir('output')

namesList=[]
scoutFound=False
for scoutID in scoutIDs:
    names={'last':None,'first':None,'file':None,'idle':False}
    # Store all data for given scout into a new table
    scout_data = scoutbook[(scoutbook['BSA Member ID'] == scoutID)].copy()
    
    # Get scouts name
    last_name = scout_data['Last Name'].loc[scout_data.index[0]]
    first_name = scout_data['First Name'].loc[scout_data.index[0]]

    approved_ranks = scout_data[(scout_data['Advancement Type']=='Rank') & (scout_data['Approved']==1)].copy()
    rankup_date = approved_ranks['Date Completed'].max()
    rank = list(approved_ranks['Advancement'].loc[approved_ranks['Date Completed']==rankup_date])
    # Some scouts may have multiple ranks recorded on the same date
    # The following uses the rankfile dictionary to find the highest rank and select that one
    # If no rank was found, the rank is set to No Rank
    if len(rank) > 1:
        for key in rankfile.keys():
            if key in rank:
                rank.remove(key)
                break
    if len(rank) == 0:
        rank = "No Rank"
    else:
        rank = rank[0]

    print("Processing %s, %s."%(last_name, first_name))
    names['last']=last_name
    names['first']=first_name
    names['file']="%s_%s.html" % (last_name,first_name)
    doc = dominate.document(title='%s %s Progress Report' % (first_name,last_name))
    with doc.head:
        # Include link to optional style sheet
        if stylesheet:
            link(rel='stylesheet',href=stylesheet)
        else:
            style(default_style)
    with doc:
        with div(cls='page'):
            with div(cls='namerank'):
                h2("%s, %s:" %(last_name,first_name),cls='name')
                if not cubs and rank in cub_rank_reqs:
                    h2("No Rank",cls='rank')
                else:
                    img(src=os.path.join('img',rankfile[rank]), onerror='this.style.display=\'none\'', alt='', cls='rank_logo')
                    h2(" %s (%s)" %(rank,str(rankup_date.date())),cls='rank')
            hr()
            # Remove old requirement for completed ranks
            ranks = approved_ranks['Advancement'].unique()
            for rank in ranks:
                rank_req=rank+" Rank Requirement"
                if scout_data[(scout_data['Advancement Type']==rank_req) & (scout_data['Approved']==0)].shape[0] > 0:
                    warn("%s, %s has unapproved %s requirement(s)" %(last_name,first_name,rank))

                scout_data = scout_data[(scout_data['Advancement Type'].str.contains(re.escape(rank))==False)]

            # Remove old requirements for completed merit badges, awards, and adventures
            for advancement in ['Merit Badge', 'Award', 'Adventure']:
                ###################################
                # First remove all approved items
                ###################################
                approved = scout_data[(scout_data['Advancement Type']==advancement) & (scout_data['Approved']==1)]
                items = approved['Advancement'].unique()
                for item in items:
                    item+=" #"
                    if scout_data[(scout_data['Advancement Type']==advancement+' Requirement') & (scout_data['Advancement'].str.contains(re.escape(item))) & (scout_data['Approved']==0)].shape[0] > 0:
                       warn("%s, %s has unapproved %s requirement(s)" %(last_name,first_name,item[:-2]))

                    scout_data = scout_data[(scout_data['Advancement'].str.contains(re.escape(item))==False)]

                ###################################
                # Next remove all completed items
                ###################################
                completed = scout_data[(scout_data['Advancement Type']==advancement) & (scout_data['Approved']==0) & (scout_data['Date Completed'].isnull()==False)]
                items = completed['Advancement'].unique()
                for item in items:
                    item+=" #"
                    # Dont print warning. Scout has item completed but is waiting for approval
                    scout_data = scout_data[(scout_data['Advancement'].str.contains(re.escape(item))==False)]

            if cubs:
                ###################################
                # Get Status of All Adventures
                ###################################
                # Get adventure list
                adventures = scout_data[(scout_data['Advancement Type'] == 'Adventure')]
                    
                # Sort Adventuress into lists of approved, complete, or in progress
                adventure_status={'Approved':None,'Complete':None,'In Progress':None}
                adventure_status['Approved'] = list(adventures['Advancement'].loc[adventures['Approved']==1].unique())
                adventure_status['Complete'] = list(adventures['Advancement'].loc[adventures['Approved']==0].unique())

                adventure_reqs = scout_data[scout_data['Advancement Type']=='Adventure Requirement'].copy()
                if adventure_reqs.shape[0] > 0:
                    adventure_reqs[['Advancement','Requirement']] = adventure_reqs['Advancement'].str.split(' #',expand=True)
                    adventure_status['In Progress'] = list(adventure_reqs['Advancement'].unique())
                else:
                    adventure_status['In Progress'] = list()
            else:
                ###################################
                # Get Status of All Merit Badges
                ###################################
                # Get merit badge list
                merit_badges = scout_data[(scout_data['Advancement Type'] == 'Merit Badge')]
                    
                # Sort MBs into lists of approved, complete, or in progress
                mb_status={'Approved':None,'Complete':None,'In Progress':None}
                mb_status['Approved'] = list(merit_badges['Advancement'].loc[merit_badges['Approved']==1].unique())
                mb_status['Complete'] = list(merit_badges['Advancement'].loc[merit_badges['Approved']==0].unique())

                mb_reqs = scout_data[scout_data['Advancement Type']=='Merit Badge Requirement'].copy()
                if mb_reqs.shape[0] > 0:
                    mb_reqs[['Advancement','Requirement']] = mb_reqs['Advancement'].str.split(' #',expand=True)
                    mb_status['In Progress'] = list(mb_reqs['Advancement'].unique())
                else:
                    mb_status['In Progress'] = list()

            if cubs:
                # TODO: should anything be displayed here? ie elective and required adventures?
                pass
            else:
                #
                # This next part is a little ugly. Threr is no clean way to get the counts using
                # pandas while simultaniously supporting the "pick one" nature of some eagle req MBs
                #

                # Get the present status of all Eagle required MBs
                eagle_mb_status = list()
                for x,sub_list in enumerate(eagle_mbs):
                    eagle_mb_status += [[None]*len(sub_list)]
                    for y,mb in enumerate(sub_list):
                        for status in ['Approved','Complete','In Progress']:
                            if mb in mb_status[status]:
                                eagle_mb_status[x][y] = status

                # Count how many Eagle required MBs are approved, complete, and in progress
                # If progress has been made on multiple MBs from a "pick one" group, then
                # count the first one and treat all others as electives.
                mb_eagle_cnt={'Required':14,'Approved':0,'Complete':0,'In Progress':0}
                for x,sub_list in enumerate(eagle_mbs):
                    if len(sub_list) == 1:
                        for status in ['Approved','Complete','In Progress']:
                            if eagle_mb_status[x][0] == status:
                                mb_eagle_cnt[status]+=1
                    else:
                        temp_cnt={'Approved':0,'Complete':0,'In Progress':0}
                        for y,mb in enumerate(sub_list):
                            for status in ['Approved','Complete','In Progress']:
                                if eagle_mb_status[x][y] == status:
                                    temp_cnt[status]+=1
                        if temp_cnt['Approved']>0:
                            mb_eagle_cnt['Approved']+=1
                        elif temp_cnt['Complete']>0:
                            mb_eagle_cnt['Complete']+=1
                        elif temp_cnt['In Progress']>0:
                            mb_eagle_cnt['In Progress']+=1

                # Count how many elective MBs are approved, complete, and in progress    
                mb_elective_cnt={'Required':7,'Approved':0,'Complete':0,'In Progress':0}
                for status in ['Approved','Complete','In Progress']:
                    mb_elective_cnt[status] = len(mb_status[status]) - mb_eagle_cnt[status]                   

                with div(cls='eagle_reqs'):
                    p("Eagle MBs = %s/%s (%s in progess)" %(mb_eagle_cnt['Approved'],mb_eagle_cnt['Required'],mb_eagle_cnt['Complete']+mb_eagle_cnt['In Progress']))
                    p("Elective MBs = %s/%s (%s in progress)" %(mb_elective_cnt['Approved'],mb_elective_cnt['Required'],mb_elective_cnt['Complete']+mb_elective_cnt['In Progress']))

            # Search scout record for entried completed since last review
            recent_entries = len(scout_data['Date Completed'].loc[scout_data['Date Completed'] > last_review])          
            if recent_entries == 0:
                names['idle']=True

            with div(cls='recent_progess'):
                if last_review != default_date:
                    h3("Progress Since %s" % str(last_review.date()))
                elif cubs:
                    h3("Progress Since Joining Cub Scouts")
                else:
                    h3("Progress Since Joining Scouts BSA")


                ###################################
                # Find newly approved ranks
                ###################################
                new_ranks=list(approved_ranks['Advancement'].loc[approved_ranks['Date Completed'] > last_review])
                if not cubs:
                    for i in range(len(new_ranks)-1,-1,-1):
                        if new_ranks[i] in cub_rank_reqs:
                            new_ranks.pop(i)

                print_list('recent_rankups',"Recent Rankup(s)",new_ranks)

                if cubs:
                    ###################################
                    # Find newly approved Adventures
                    ###################################
                    new_adventures=list(adventures['Advancement'].loc[adventures['Date Completed'] > last_review])
                    print_list('approved_adventures',"Recently Approved Adventures",new_adventures)

                    ###################################
                    # Find completed Adventures waiting for approval
                    ###################################
                    complete_adventures = list(scout_data['Advancement'].loc[(scout_data['Advancement Type']=='Adventure')&(scout_data['Approved']==0)])
                    print_list('complete_adventures',"Complete Adventures Awaiting Approval",complete_adventures)


                else:
                    ###################################
                    # Find newly approved MBs
                    ###################################
                    new_mbs=list(merit_badges['Advancement'].loc[merit_badges['Date Completed'] > last_review])
                    print_list('approved_mbs',"Recently Approved Merit Badges",new_mbs)

                    ###################################
                    # Find completed MBs waiting for approval
                    ###################################
                    complete_mbs = list(scout_data['Advancement'].loc[(scout_data['Advancement Type']=='Merit Badge')&(scout_data['Approved']==0)])
                    print_list('complete_mbs',"Complete MBs Awaiting Approval",complete_mbs)


                ###################################
                # Find newly approved Awards
                ###################################
                awards = scout_data[(scout_data['Advancement Type'] == 'Award')]
                new_awards=list(awards['Advancement'].loc[awards['Date Completed'] > last_review])
                print_list('approved_awards',"Recently Approved Awards",new_awards)

            ###################################
            # Find progress on individual requirements
            ###################################
            rank_requirements=scout_data[(scout_data['Advancement Type'].str.contains('Rank Requirement'))].copy()
            rank_requirements['Requirement'] = rank_requirements.loc[:, 'Advancement']
            other_requirements=scout_data[~(scout_data['Advancement Type'].str.contains('Rank Requirement')) & (scout_data['Advancement Type'].str.contains('Requirement')) ].copy()
            if other_requirements.shape[0]>0:
                other_requirements[['Advancement','Requirement']] = other_requirements['Advancement'].str.split(' #',n=1,expand=True)
            else:
                rank_requirements['Requirement'] = rank_requirements.loc[:, 'Advancement']

            requirements=pandas.concat([rank_requirements,other_requirements],ignore_index=True)
            
            ###################################
            # Divide requirments by approval status and completion date
            ###################################
            approved=requirements[(requirements['Approved']==1)]
            unapproved=requirements[(requirements['Approved']==0)]
            prev_approved=approved[(approved['Date Completed'] <= last_review)]
            newly_approved=approved[(approved['Date Completed'] > last_review)]

            ####
            # Loop through each rank with some requirements completed
            ####
            with div(cls='requirement_progress'):
                h3("Requirement Progress")

                rank_reqs = list(approved['Advancement Type'].loc[approved['Advancement Type'].str.contains('Rank Requirement')].unique())
                if not cubs:
                    for i in range(len(rank_reqs)-1,-1,-1):
                        if rank_reqs[i][:-17] in cub_rank_reqs:
                            rank_reqs.pop(i)

                with div(cls='rank_progress'):
                    h4("Rank Progress")
                    # For each rank with approved requirements
                    if len(rank_reqs) == 0:
                        p("None")
                    else:
                        for rank in rank_reqs:
                            new_reqs = list(newly_approved['Advancement'].loc[newly_approved['Advancement Type'].str.contains(re.escape(rank))])
                            new_reqs.sort()
                            prev_reqs = list(prev_approved['Advancement'].loc[prev_approved['Advancement Type'].str.contains(re.escape(rank))])
                            prev_reqs.sort()
                            try:
                                if cubs:
                                    all_reqs = cub_rank_reqs[rank[:-17]]
                                else:
                                    all_reqs = bsa_rank_reqs[rank[:-17]]
                            except:
                                warn("%s rank not yet supported by this tool"%rank[:-17])
                            s=set(new_reqs)
                            reqs_remaining=[req for req in all_reqs if req not in s]
                            s=set(prev_reqs)
                            reqs_remaining=[req for req in reqs_remaining if req not in s]

                            # Print completed reqs
                            print_reqs(rank,new_reqs,prev_reqs,reqs_remaining)
            
                if cubs:
                    with div(cls='adventure_progress'):
                        h4("Adventure Progress")    
                        ####
                        # Loop through each Adventure with some requirements completed
                        ####
                        approved_reqs = approved[approved['Advancement Type']=='Adventure Requirement'].copy()

                        if approved_reqs.shape[0] > 0:
                            adventure_reqs = list(approved_reqs['Advancement'].unique())
                        else:
                            adventure_reqs = list()

                        if len(adventure_reqs) == 0:
                            p("None")
                        else:
                            # For each adventure with approved requirements
                            for adventure in adventure_reqs:
                                new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(adventure))])
                                new_reqs.sort()
                                prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(adventure))])
                                prev_reqs.sort()
                                #The following are not alwayr present in scoutbook, do not use
                                #reqs_remaining = list(unapproved['Requirement'].loc[unapproved['Advancement'].str.contains(re.escape(adventure))])
                                #reqs_remaining.sort()

                                # Print completed reqs
                                print_reqs(adventure,new_reqs,prev_reqs,None)

                else:
                    with div(cls='mb_progress'):
                        h4("MB Progress")
                        ####
                        # Loop through each MB with some requirements completed
                        ####
                        approved_reqs = approved[approved['Advancement Type']=='Merit Badge Requirement'].copy()
                        if approved_reqs.shape[0] > 0:
                            mb_reqs = list(approved_reqs['Advancement'].unique())
                        else:
                            mb_reqs = list()

                        if len(mb_reqs) == 0:
                            p("None")
                        else:
                            # For each mb with approved requirements
                            for mb in mb_reqs:
                                new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(mb))])
                                new_reqs.sort()
                                prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(mb))])
                                prev_reqs.sort()
                                #The following are not alwayr present in scoutbook, do not use
                                #reqs_remaining = list(unapproved['Requirement'].loc[unapproved['Advancement'].str.contains(re.escape(mb))])
                                #reqs_remaining.sort()

                                # Print completed reqs                            
                                print_reqs(mb,new_reqs,prev_reqs,None)

                with div(cls='award_progress'):   
                    h4("Award Progress")    
                    ####
                    # Loop through each Award with some requirements completed
                    ####
                    approved_reqs = approved[approved['Advancement Type']=='Award Requirement'].copy()
                    if approved_reqs.shape[0] > 0:
                        award_reqs = list(approved_reqs['Advancement'].unique())
                        if not cubs:
                            for i in range(len(award_reqs)-1,-1,-1):
                                if award_reqs[i].startswith('Cub Scout') or award_reqs[i].startswith('Webelo'):
                                    award_reqs.pop(i)
                    else:
                        award_reqs = list()

                    if len(award_reqs) == 0:
                        p("None")
                    else:
                        # For each award with approved requirements
                        for award in award_reqs:
                            new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(award))])
                            new_reqs.sort()
                            prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(award))])
                            prev_reqs.sort()

                            # Print completed reqs
                            print_reqs(award,new_reqs,prev_reqs,None)

    with open(names['file'], 'w') as file:
        file.write(doc.render())
    namesList.append(names)

doc = dominate.document(title='Scout Progress Reports')
with doc.head:
    # Include link to optional style sheet
    if stylesheet:
        link(rel='stylesheet',href=stylesheet)
    else:
        style(default_style)
with doc:
    with div(cls='page'):
        h2("Progressing Scouts")
        with div(cls='toc').add(ol()):
            for names in namesList:
                if not names['idle']:
                    li(a("%s %s"%(names['first'],names['last']), href=names['file']))
        h2("Idle Scouts")
        with div(cls='toc').add(ol()):
            for names in namesList:
                if names['idle']:
                    li(a("%s %s"%(names['first'],names['last']), href=names['file']))

with open('index.html', 'w') as file:
    file.write(doc.render())

print("Opening output in browser")
webbrowser.open('file://'+os.path.realpath('index.html'))

#if windows:
#    input("\nPress any key to continue...")
