# this code gathers a random sample from a subset of patents
# to be used in evaluating the recall of the keyword filering rule

import json, requests, random, csv

# identify the most common cpc_group_id
groups = {}
#open the file that contains the list of patents
f=open("clean_patents_info.json","r")
data=f.read()
f.close()
patents=json.loads(data)
for patent in patents:
    for group in patent['cpcs']:
        if group['cpc_group_id'] not in groups:
            groups[group['cpc_group_id']]=1
        else:
            groups[group['cpc_group_id']]+=1


group_id = max(groups, key=groups.get) # this gives H04L

patents = []
for page in range(1,11):
    # gather all patents filed after 1989 that fall within the class H04L - 	TRANSMISSION OF DIGITAL INFORMATION
    # request to the patentsview API
    result=requests.get('http://www.patentsview.org/api/patents/query?q={"_and": [{"_gte":{"app_date":"1990-01-01"}}, {"_lt":{"app_date":"2014-01-01"}},{"cpc_group_id":"H04L"}]}&f=["patent_number","patent_title","patent_abstract","app_date","cpc_subsection_id"]&o={"page":'+str(page)+',"per_page":10000}')
    # result.status_code
    # result.headers
    info=json.loads(result.content.decode())
    for patent in info['patents']:
        patents.append(patent)

# generate a random selection of 400 patents
rand_pats = []
random.seed(15)
for x in range(400):
  rand_pats.append(patents[random.randint(0,len(patents))])

patents_dict = {'patent':[]}
for pat in rand_pats:
    patents_dict['patent'].append(pat)
for pat in patents_dict['patent']:
    # Convert to True as necessary after manual checks
    pat['relevance']='False'

# write JSON data to file
with open('rand_sample.json', 'w') as f:
    json.dump(patents_dict, f)
    
# make a simpler version in CSV format for manual checking
with open('rand_sample.csv', 'w', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for patent in patents_dict['patent']:
        writer.writerow([patent['patent_title'],patent['patent_abstract'], patent['patent_number']])

# manually checked sample
# the 'relevance' variable specifies 'True' if patent is relevant
import keyword_function
f=open("rand_sample_annotated.json","r")
data=f.read()
f.close()
patents_anot=json.loads(data)
alg_pats = [] # relevant patents identified by algorithm
man_pats = [] # relevant patents identified manually
for patent in patents_anot['patent']:
    abstract=patent['patent_abstract']
    title=patent['patent_title']
    # combine patent title and abtract into one block of text
    tx = title + ' '+ abstract
    # look for keyword matches
    if keyword_function.keywordFinder(text = tx)==True:
        alg_pats.append(patent['patent_number'])
    if patent['relevance'] == "True":
        man_pats.append(patent['patent_number'])