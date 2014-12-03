import pandas as pd
import numpy as np
import os, sys
#from copy import deepcopy
import glob









#ESTABLISH INPUT ARGUMENTS
input_folder = '/home/alex/GIT/tasks/aiddata_2014-12-02-13-56'
output_folder = '/home/alex/Desktop/combine-dedup-results'
file_wildcard = '*.csv'

#CALL FUNCTION
#dedup_and_concat(input_folder, file_wildcard)


if not os.path.exists(output_folder):
    os.makedirs(output_folder)




#startTime = datetime.now()

#def dedup_and_concat(input_folder, file_wildcard):
    #if not os.path.exists(output_folder):
        #os.makedirs(output_folder)

    #ESTABLISHES LIST OF FILEPATHS
wildcard_filepath = os.path.join(input_folder, file_wildcard)
filepaths_list = glob.glob(wildcard_filepath)

    #SPA MASTER PRODUCTS

sectorlist = ['Title', 'Short Description', 'Long Description', 'AidData Sector Code']
purposelist = ['Title', 'Short Description', 'Long Description', 'AidData Purpose Code']
activitylist = ['Title', 'Short Description', 'Long Description', 'AidData Activity Code(s)']

master_df_s = pd.DataFrame(columns=sectorlist)
master_df_p = pd.DataFrame(columns=purposelist)
master_df_a = pd.DataFrame(columns=activitylist)


def stringsort(x):
    entry = x['AidData Activity Code(s)']
    if isinstance(entry, str):
        if '|' in entry:
            code_list = entry.split('|')
            code_list.sort()
            entry = '|'.join(code_list)
            return entry

x = 0
#filepaths_list = [filepaths_list[0]]
for filepath in filepaths_list:
    x = x + 1
    #print x
    #filepath = filepaths_list[0]
    file = pd.read_csv(filepath, quotechar='\"')

        #ELIMINATE ROWS WITH NO ACTIVITY CODES
        #(DIFFERENTIATES BETWEEN ACTIVITY CODES AND nan VALUES BY >=0)
    #file = file[file['AidData Activity Code(s)'] >= 0]
    #series = file['AidData Activity Code(s)']
    file['AidData Activity Code(s)'] = file.apply(stringsort, axis=1)


#    test_list = []

    #for entry in series:
#        if isinstance(entry, str):
#            if '|' in entry:
#                code_list = entry.split('|')
#                code_list.sort()
#                entry = '|'.join(code_list)
#                test_list.append(entry)
#            else:
#                test_list.append(entry)
#        else: test_list.append(entry)


    #test = pd.Series(test_list)

    #file["AidData Activity Code(s)"] = pd.Series(test_list)

    file_s = file[sectorlist]
    file_s = file_s.dropna(subset=["AidData Sector Code"], how='any')

    file_p = file[purposelist]
    file_p = file_p.dropna(subset=["AidData Purpose Code"], how='any')

    file_a = file[activitylist]
    file_a = file_a.dropna(subset=["AidData Activity Code(s)"], how='any')


    master_df_s = master_df_s.append(file_s)
    master_df_p = master_df_p.append(file_p)
    master_df_a = master_df_a.append(file_a)

sector_df = master_df_s.drop_duplicates()
project_df = master_df_p.drop_duplicates()
activity_df = master_df_a.drop_duplicates()

sector_df.to_csv((os.path.join(output_folder, 'sector_data.csv')))
project_df.to_csv((os.path.join(output_folder, 'project_data.csv')))
activity_df.to_csv((os.path.join(output_folder, 'activity_data.csv')))
