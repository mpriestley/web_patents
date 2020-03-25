# identify misspelled or duplicate assignee names using similarity matching

# assignee labels may have multiple entries that relate to the same company,
# where some entries have a slightly different spelling then the other.
# We want to de-duplicate these.

# approach inspired by https://github.com/Cheukting/fuzzy-match-company-name/blob/master/Fuzzy-match-company-names.ipynb

import re, json, csv
import pandas as pd
import numpy as np
from collections import Counter

# Function to find all close matches of  
# input string in given list of possible strings 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def clean_text(words, text):
    for word in words:
        text = text.replace(word, '')
    return text


assignees = []

#open the file that contains the list of patents
f=open("patents_fulltext_standards_social.json","r")
data=f.read()
f.close()
patents=json.loads(data)

for patent in patents:
    company=patent['assignees'][0]['assignee_organization']
    if company != None and company not in assignees:
        assignees.append(company)

# find most common words (e.g. company, corporation)
names_freq = Counter()
for name in assignees:
    names_freq.update(str(name).split(" "))
key_words = [word for (word,_) in names_freq.most_common(40)]
print(key_words)

# group names by their first character
# because matching all pairs at once takes too long
all_main_name = pd.DataFrame(columns=['sort_gp','names','alias','score'])
assignees.sort()
all_main_name['names'] = assignees
all_main_name['sort_gp'] = all_main_name['names'].apply(lambda x: x[0])

all_sort_gp = all_main_name['sort_gp'].unique()

for sortgp in all_sort_gp:
    this_gp = all_main_name.groupby(['sort_gp']).get_group(sortgp)
    gp_start = this_gp.index.min()
    gp_end = this_gp.index.max()
    for i in range(gp_start,gp_end+1):
    
        # if self has not got alias, asign to be alias of itself
        if pd.isna(all_main_name['alias'].iloc[i]):
            all_main_name['alias'].iloc[i] = all_main_name['names'].iloc[i]
            all_main_name['score'].iloc[i] = 100
        
        # if the following has not got alias and fuzzy match, asign to be alias of this one
        for j in range(i+1,gp_end+1):
            if pd.isna(all_main_name['alias'].iloc[j]):
                # compare strings with common words removed
                fuzz_socre = fuzz.token_set_ratio(clean_text(key_words,all_main_name['names'].iloc[i]),clean_text(key_words,all_main_name['names'].iloc[j]))
                if (fuzz_socre > 85):
                    all_main_name['alias'].iloc[j] = all_main_name['alias'].iloc[i]
                    all_main_name['score'].iloc[j] = fuzz_socre

        if i % (len(assignees)//10) == 0:
            print("progress: %.2f" % (100*i/len(assignees)) + "%")
all_main_name = all_main_name[(all_main_name['names']!=all_main_name['alias']) & (all_main_name['alias'].notna())]
all_main_name.to_csv('company_aliases.csv')

# manually edited list of name changes required
# key: zero means no match, number means whether name (1) or alias (2) is correct.
# Else, correct name is added.
# company IBM and AOL acronyms also changed
changes_table = pd.read_csv("company_aliases_manual.csv", index_col=0)
# store changes in a dict (bad name: correction)
changes = {}
for index, row in changes_table.iterrows():
    comp1 = row['names']
    comp2 = row['alias']
    change = row['check']
    if change == '1':
        changes[comp2] = comp1
    elif change == '2':
        changes[comp1] = comp2
    elif change != '0':
        changes[comp1] = change
        changes[comp2] = change

# now clean the assignee names in the dataset  
affected_patents = 0 # count of affected patents
for patent in patents:
    company=patent['assignees'][0]['assignee_organization']
    if company != None and company in changes:
        patent['assignees'][0]['assignee_organization'] = changes[company]
        affected_patents += 1

# write JSON data to file
with open("patents_final.json", "w") as fp:
    json.dump(patents, fp)