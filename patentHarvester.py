# this code harvests additional information for the relevant patents using the PatentsView API
# (e.g. CPC classifications, citations and assignees)
# requires relevant_patents.json
# returns relevant_patents_info.json

import json, requests

#open the file that contains the list of patents
f=open("relevant_patents.json","r")
data=f.read()
f.close()
patents=json.loads(data)['patents']
#dict to store new data
patents_info ={}
patents_info['patents']=[]

# array for relevant patent numbers
numbers =[]
# irrelevant patent numbers, collated manually
irrel = ['5544320','5570084','5696901','5745753','5935637','5958137','5980442','7247391',
         '7261217','9096973','5974444','6312523','6470446','6497383','7497399','8113377',
         '8317054','8635352','9220297','9432813','6536705','6588866','6799083','6875308',
         '6908531','7021482','7114627','7462259']

for patent in patents:
    number = patent['id']
    if number not in irrel:
        numbers.append(number)
        
# chunk patents list into API friendly sizes
# function from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
api_chunks = chunks(numbers, 50)
harvested_patents = [] # keep track in case anything goes wrong
# request the results in batches, due to query length restrictions
for chunk in api_chunks:
    # request to the PatentsView API
    result=requests.get('http://www.patentsview.org/api/patents/query?q={"patent_number":'+str(chunk).replace('\'', '"')+'}&f=["cpc_subgroup_id","cpc_subsection_id","cpc_group_id","cpc_sequence","patent_number","patent_title","patent_abstract","cited_patent_number","app_date","assignee_country","assignee_organization","inventor_id","assignee_id"]&o={"per_page":50}')
    info=json.loads(result.content.decode())['patents']
    # append each patent that is returned
    for i in info:
        patents_info['patents'].append(i)
        harvested_patents.append(i['patent_number'])
# check for any missing patents
if len(numbers)>len(harvested_patents):
    problem_patents = set(numbers).difference(harvested_patents)
    # try again to download them individually
    for pat in problem_patents:
        result=requests.get('http://www.patentsview.org/api/patents/query?q={"patent_number":'+str(pat)+'}&f=["cpc_subgroup_id","cpc_subsection_id","cpc_group_id","cpc_sequence","patent_number","patent_title","patent_abstract","cited_patent_number","app_date","assignee_country","assignee_organization","inventor_id","assignee_id"]&o={"per_page":50}')
        info=json.loads(result.content.decode())['patents'][0]
        patents_info['patents'].append(info)
        harvested_patents.append(info['patent_number'])
print("Total number of patents harvested: ",len(harvested_patents))
print("Total number of patents that couldn't be harvested: ",len(set(numbers).difference(harvested_patents)))

# write JSON data to file
with open("relevant_patents_info.json", "w") as fp:
    json.dump(patents_info, fp)