#!/usr/bin/env python
###########################################################
"Scout Progress Report Generator"

__author__     = "Steven Greasby"
__copyright__  = "Copyright (C) 2022 Steven Greasby"
__license__    = "GPL 2.0"
__url__        = "http://github.com/sgreasby/Scout-Progress-Report"
__maintainer__ = "Steven Greasby"
###########################################################
import sys
import pandas
import re
import datetime
import builtins

warnings=False

PRINT_COLS=50

pandas.set_option('display.max_rows', None)
#pandas.set_option('display.max_columns', None)

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

#TODO:Are these right?
cub_rank_req={'Bobcat'          :['1','2','3','4','5','6','7'],
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
               'Star'           :['1','2','3','4','5','6','7','8'],
               'Life'           :['1','2','3','4','5','6','7','8'],
               'Eagle'          :['1','2','3','4','5','6','7']}

indent=0
def print(*args, **kwargs):
    builtins.print("  "*indent,end="")
    return builtins.print(*args, **kwargs)

def warn(*args, **kwargs):
    if warnings:
        builtins.print("WARNING:",end="")
        return builtins.print(*args, **kwargs)
    else:
        return True

def error(*args, **kwargs):
    builtins.print("ERROR:",end="")
    return builtins.print(*args, **kwargs)

def usage():
    builtins.print("Usage: %s {--date=[MM/DD/YYYY]} {--id=[scoutid]} {--cubs} [scoutbook.csv]\n\n" %(sys.argv[0]))
    sys.exit()

# Parse Arguments
csv_open=False
# Use pandas to convert last_review to datetime object
last_review="1/1/1980"
last_review=pandas.to_datetime([last_review])[0]
specificScout=False
cubs=False
if len(sys.argv)<2:
    usage()
for arg in sys.argv[1:]:
    if arg.startswith('--date='):
        junk,last_review = arg.split('=')
        try:
            # Use pandas to convert last_review to datetime object
            last_review=pandas.to_datetime([last_review])[0]
        except:
            builtins.print("%s does not appear to be a valid date."%last_review)
            usage()
    elif arg.startswith('--id='):
        junk,specificScout = arg.split('=')
        try:
            specificScout=int(specificScout)
        except:
            builtins.print("%s does not appear to be a valid scout ID"%specificScout)
            usage()
    elif arg == '--cubs':
        cubs=True
    elif not arg.startswith('--'):
        builtins.print("Opening %s" %(arg))
    
        try:
            # First row of CSV contains column names.
            # However some rows have an undocumnted column
            # Add dummy column to avoid errors when reading in data
            cols = pandas.read_csv(arg, nrows=1,header=None).values.flatten().tolist()+['Undocumented']
        except:
            builtins.print("Failed to read %s." %(arg))
            usage()
        else:
            csv_open=True

        # read the rest of the CSV file
        # Skip first row (col names) and use names determined above
        scoutbook = pandas.read_csv(arg, skiprows=1,names=cols)
    else:
        usage()

if not csv_open:
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

scoutFound=False
for scoutID in scoutIDs:
    if specificScout:
        if scoutFound:
            break
        elif scoutID == specificScout:
            scoutFound = True
        else:
            continue
    print("")

    # Store all data for given scout into a new table
    scout_data = scoutbook[(scoutbook['BSA Member ID'] == scoutID)].copy()
    
    # Get scouts name
    last_name = scout_data['Last Name'].loc[scout_data.index[0]]
    first_name = scout_data['First Name'].loc[scout_data.index[0]]

    approved_ranks = scout_data[(scout_data['Advancement Type']=='Rank') & (scout_data['Approved']==1)].copy()
    rankup_date = approved_ranks['Date Completed'].max()
    rank = approved_ranks['Advancement'].loc[approved_ranks['Date Completed']==rankup_date].to_string(index=False)
    
    indent=0
    print("%s, %s: %s (%s)" %(last_name,first_name,rank,str(rankup_date.date())))
    
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

        indent=1
        print("Eagle MBs = %s/%s (%s in progess)" %(mb_eagle_cnt['Approved'],mb_eagle_cnt['Required'],mb_eagle_cnt['Complete']+mb_eagle_cnt['In Progress']))
        print("Elective MBs = %s/%s (%s in progress)" %(mb_elective_cnt['Approved'],mb_elective_cnt['Required'],mb_elective_cnt['Complete']+mb_elective_cnt['In Progress']))
        print("")

    ###################################
    # Find newly approved ranks
    ###################################
    new_ranks=list(approved_ranks['Advancement'].loc[approved_ranks['Date Completed'] > last_review])
    indent=1
    print("Recent Rankup(s)")
    indent=2
    if len(new_ranks) == 0:
        print("None")
    else:
        for rank in new_ranks:
            print("%s" %(rank))

    if cubs:
        ###################################
        # Find newly approved Adventures
        ###################################
        new_adventures=list(adventures['Advancement'].loc[adventures['Date Completed'] > last_review])
        indent=1
        print("Recently Approved Adventures")
        indent=2
        if len(new_adventures) == 0:
            print("None")
        else:
            for adventure in new_adventures:
                print("%s" %(adventure))

        ###################################
        # Find completed Adventures waiting for approval
        ###################################
        complete_adventures = list(scout_data['Advancement'].loc[(scout_data['Advancement Type']=='Adventure')&(scout_data['Approved']==0)])
        indent=1
        print("Complete Adventures Awaiting Approval")
        indent=2
        if len(complete_adventures) == 0:
            print("None")
        else:
            for adventure in complete_adventures:
                print(adventure)
    else:
        ###################################
        # Find newly approved MBs
        ###################################
        new_mbs=list(merit_badges['Advancement'].loc[merit_badges['Date Completed'] > last_review])
        indent=1
        print("Recently Approved Merit Badges")
        indent=2
        if len(new_mbs) == 0:
            print("None")
        else:
            for mb in new_mbs:
                print("%s" %(mb))

        ###################################
        # Find completed MBs waiting for approval
        ###################################
        complete_mbs = list(scout_data['Advancement'].loc[(scout_data['Advancement Type']=='Merit Badge')&(scout_data['Approved']==0)])
        indent=1
        print("Complete MBs Awaiting Approval")
        indent=2
        if len(complete_mbs) == 0:
            print("None")
        else:
            for mb in complete_mbs:
                print(mb)

    ###################################
    # Find newly approved Awards
    ###################################
    awards = scout_data[(scout_data['Advancement Type'] == 'Award')]
    new_awards=list(awards['Advancement'].loc[awards['Date Completed'] > last_review])
    indent=1
    print("Recently Approved Awards")
    indent=2
    if len(new_awards) == 0:
        print("None")
    else:
        for award in new_awards:
            print("%s" %(award))

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
    if requirements.shape[0]==0:
        #TODO:print that no progress has ever been recorded
        continue
    
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
    indent=1
    print("")
    print("Requirement Progress")

    rank_reqs = list(approved['Advancement Type'].loc[approved['Advancement Type'].str.contains('Rank Requirement')].unique())
    indent=2
    print("Rank Progress")    
    indent=3
    # For each rank with approved requirements
    if len(rank_reqs) == 0:
        print("None")
    else:
        for rank in rank_reqs:
            print("%ss" %(rank))
            # Print reqs recently completed
            new_reqs = list(newly_approved['Advancement'].loc[newly_approved['Advancement Type'].str.contains(re.escape(rank))])
            new_reqs.sort()
            indent=4
            print("Recently Completed")
            indent=5
            if len(new_reqs) >0:
                for i in range(0,len(new_reqs),PRINT_COLS):
                    print(*new_reqs[i:i+PRINT_COLS], sep = "  ")
            else:
                print("None")

            # Print reqs previously completed
            prev_reqs = list(prev_approved['Advancement'].loc[prev_approved['Advancement Type'].str.contains(re.escape(rank))])
            prev_reqs.sort()
            indent=4
            print("Previously Completed")
            indent=5
            if len(prev_reqs) > 0:
                for i in range(0,len(prev_reqs),PRINT_COLS):
                    print(*prev_reqs[i:i+PRINT_COLS], sep = "  ")
            else:
                print("None")

            # Print reqs left to complete
            try:
                if cubs:
                    all_reqs = cub_rank_reks[rank[:-17]]
                else:
                    all_reqs = bsa_rank_reqs[rank[:-17]]
            except:
                builtins.print("Warning: %s rank not yet supported"%rank[:-17])
            s=set(new_reqs)
            reqs_remaining=[req for req in all_reqs if req not in s]
            s=set(prev_reqs)
            reqs_remaining=[req for req in reqs_remaining if req not in s]
            indent=4
            print("Remaining")
            indent=5
            if len(reqs_remaining) > 0:
                for i in range(0,len(reqs_remaining),PRINT_COLS):
                    print(*reqs_remaining[i:i+PRINT_COLS], sep = "  ")
            else:
                print("None")

    if cubs:
        indent=2
        print("Adventure Progress")    
        ####
        # Loop throough each Adventure with some requirements completed
        ####
        approved_reqs = approved[approved['Advancement Type']=='Adventure Requirement'].copy()

        if approved_reqs.shape[0] > 0:
            adventure_reqs = list(approved_reqs['Advancement'].unique())
        else:
            adventure_reqs = list()

        if len(adventure_reqs) == 0:
            indent=3
            print("None")
        else:
            # For each adventure with approved requirements
            for adventure in adventure_reqs:
                indent=3
                print("%s" %(adventure))
                # Print reqs recently completed
                new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(adventure))])
                new_reqs.sort()
                indent=4
                print("Recently Completed")
                indent=5
                if len(new_reqs) >0:
                    for i in range(0,len(new_reqs),PRINT_COLS):
                        print(*new_reqs[i:i+PRINT_COLS], sep = "  ")
                else:
                    print("None")

                # Print reqs previously completed
                prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(adventure))])
                prev_reqs.sort()
                indent=4
                print("Previously Completed")
                indent=5
                if len(prev_reqs) > 0:
                    for i in range(0,len(prev_reqs),PRINT_COLS):
                        print(*prev_reqs[i:i+PRINT_COLS], sep = "  ")
                else:
                    print("None")

                # DONT DO THE FOLLOWING: Scoutbook list unapproved requriements for some Adventures but not others
                # Print reqs left to complete
                #reqs_remaining = list(unapproved['Requirement'].loc[unapproved['Advancement'].str.contains(re.escape(adventure))])
                #reqs_remaining.sort()
                #indent=4
                #print("Remaining")
                #indent=5
                #if len(reqs_remaining) > 0:
                #    for i in range(0,len(reqs_remaining),PRINT_COLS):
                #        print(*reqs_remaining[i:i+PRINT_COLS], sep = "  ")
                #else:
                #    print("None")
    else:
        indent=2
        print("MB Progress")    
        ####
        # Loop throough each MB with some requirements completed
        ####
        approved_reqs = approved[approved['Advancement Type']=='Merit Badge Requirement'].copy()
        if approved_reqs.shape[0] > 0:
            mb_reqs = list(approved_reqs['Advancement'].unique())
        else:
            mb_reqs = list()

        if len(mb_reqs) == 0:
            indent=3
            print("None")
        else:
            # For each mb with approved requirements
            for mb in mb_reqs:
                indent=3
                print("%s" %(mb))
                # Print reqs recently completed
                new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(mb))])
                new_reqs.sort()
                indent=4
                print("Recently Completed")
                indent=5
                if len(new_reqs) >0:
                    for i in range(0,len(new_reqs),PRINT_COLS):
                        print(*new_reqs[i:i+PRINT_COLS], sep = "  ")
                else:
                    print("None")

                # Print reqs previously completed
                prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(mb))])
                prev_reqs.sort()
                indent=4
                print("Previously Completed")
                indent=5
                if len(prev_reqs) > 0:
                    for i in range(0,len(prev_reqs),PRINT_COLS):
                        print(*prev_reqs[i:i+PRINT_COLS], sep = "  ")
                else:
                    print("None")

                # DONT DO THE FOLLOWING: Scoutbook list unapproved requriements for some MBs but not others
                # Print reqs left to complete
                #reqs_remaining = list(unapproved['Requirement'].loc[unapproved['Advancement'].str.contains(re.escape(mb))])
                #reqs_remaining.sort()
                #indent=4
                #print("Remaining")
                #indent=5
                #if len(reqs_remaining) > 0:
                #    for i in range(0,len(reqs_remaining),PRINT_COLS):
                #        print(*reqs_remaining[i:i+PRINT_COLS], sep = "  ")
                #else:
                #    print("None")

    
    indent=2
    print("Award Progress")    
    ####
    # Loop throough each Award with some requirements completed
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
        indent=3
        print("None")
    else:
        # For each award with approved requirements
        for award in award_reqs:
            indent=3
            print("%s" %(award))
            # Print reqs recently completed
            new_reqs = list(newly_approved['Requirement'].loc[newly_approved['Advancement'].str.contains(re.escape(award))])
            new_reqs.sort()
            indent=4
            print("Recently Completed")
            indent=5
            if len(new_reqs) >0:
                for i in range(0,len(new_reqs),PRINT_COLS):
                    print( *new_reqs[i:i+PRINT_COLS], sep = "  ")
            else:
                print("None")

            # Print reqs previously completed
            prev_reqs = list(prev_approved['Requirement'].loc[prev_approved['Advancement'].str.contains(re.escape(award))])
            prev_reqs.sort()
            indent=4
            print("Previously Completed")
            indent=5
            if len(prev_reqs) > 0:
                for i in range(0,len(prev_reqs),PRINT_COLS):
                    print(*prev_reqs[i:i+PRINT_COLS], sep = "  ")
            else:
                print("None")

if specificScout and not scoutFound:
    builtins.print("Scout %d not found" % specificScout)
    usage()

