import pandas as pd
import os, sys
import glob

#ESTABLISH INPUT ARGUMENTS
input_folder = '/home/alex/GIT/tasks/aiddata_2014-12-02-13-56'
output_folder = '/home/alex/Desktop/combine-dedup-results'
file_wildcard = '*.csv'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#ESTABLISH LIST OF FILEPATHS
wildcard_filepath = os.path.join(input_folder, file_wildcard)
filepaths_list = glob.glob(wildcard_filepath)

#DEFINE DATAFRAMES FOR SPA VARIANTS
sectorlist = ['Title', 'Short Description', 'Long Description', 'AidData Sector Code']
purposelist = ['Title', 'Short Description', 'Long Description', 'AidData Purpose Code']
activitylist = ['Title', 'Short Description', 'Long Description', 'AidData Activity Code(s)']

master_df_s = pd.DataFrame(columns=sectorlist)
master_df_p = pd.DataFrame(columns=purposelist)
master_df_a = pd.DataFrame(columns=activitylist)

#DEFINE FUNCTION FOR LATER SORTING OF ACTIVITY CODES
def stringsort(x):
    entry = x['AidData Activity Code(s)']
    if isinstance(entry, str):
        if '|' in entry:
            code_list = entry.split('|')
            code_list.sort()
            entry = '|'.join(code_list)
            return entry

#LOOPS OVER ALL FILES, ADDS ENTRIES TO MASTER, REMOVES RELEVENT EMPTY ROWS
#x = 0
for filepath in filepaths_list:
    #x = x + 1
    #print x
    file = pd.read_csv(filepath, quotechar='\"')

    file['AidData Activity Code(s)'] = file.apply(stringsort, axis=1)

    file_s = file[sectorlist]
    file_s = file_s.dropna(subset=["AidData Sector Code"], how='any')

    file_p = file[purposelist]
    file_p = file_p.dropna(subset=["AidData Purpose Code"], how='any')

    file_a = file[activitylist]
    file_a = file_a.dropna(subset=["AidData Activity Code(s)"], how='any')


    master_df_s = master_df_s.append(file_s)
    master_df_p = master_df_p.append(file_p)
    master_df_a = master_df_a.append(file_a)

#DROPS DUPLICATES FROM DATAFRAMES
sector_df = master_df_s.drop_duplicates()
purpose_df = master_df_p.drop_duplicates()
activity_df = master_df_a.drop_duplicates()

#CONVERTS SECTOR AND PURPOSE CODE COLUMNS TO INTEGER TYPE
sector_df[['AidData Sector Code']] = sector_df[['AidData Sector Code']].astype(int)
purpose_df[['AidData Purpose Code']] = purpose_df[['AidData Purpose Code']].astype(int)

#EXPORTS DATAFRAMES TO TSV FORMAT IN THE DESIGNATED OUTPUT FOLDER
sector_df.to_csv((os.path.join(output_folder, 'sector_data.tsv')), sep='\t', index=False)
purpose_df.to_csv((os.path.join(output_folder, 'purpose_data.tsv')), sep='\t', index=False)
activity_df.to_csv((os.path.join(output_folder, 'activity_data.tsv')), sep='\t', index=False)
