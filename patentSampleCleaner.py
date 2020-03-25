# this code sorts the patents by date
# adds a new variable only with citations to patents that are in the sample (in case we want to do network analysis later)
# adds a new simplified variable for the cpc code sequence
# adds a new simplified variable to show broader cpc classes (e.g. to infer broad or narrow invention)

import json, re
#open the file that contains the list of patents
f=open("relevant_patents_info.json","r")
data=f.read()
f.close()
patents=json.loads(data)['patents']
# sort the patents by date
patents = sorted(patents, key=lambda k: k['applications'][0]['app_date'])

# array to store the id numbers of all patents that are in the sample
# this is done to track in-sample citations
numbers=[]
to_delete=[] # for patents filed after 2013
for patent in patents:
    date = patent['applications'][0]['app_date']
    year = re.split("-", date)[0]
    # only keep patents filed before 2014
    if int(year) < 2014:
        number=patent['patent_number']
        numbers.append(number)
    else:
        to_delete.append(patent)
# delete patents filed after 2013
for i in to_delete:
    patents.remove(i)
    
for patent in patents:
    citations=patent['cited_patents']
    # citations to patents that are in the sample
    insample_citations = []
    for citation in citations:
        if citation['cited_patent_number'] in numbers:
            insample_citations.append(citation['cited_patent_number'])
    patent['insample_citations'] = insample_citations
    # combination of cpc codes
    # start with empty array
    combo = [None] * len(patent['cpcs'])
    for cpc in patent['cpcs']:
        if cpc['cpc_sequence']!=None:
            sequence_position = cpc['cpc_sequence']
            combo[int(sequence_position)] = cpc['cpc_subgroup_id']
    patent['cpc_combo'] = combo # order of CPCs is important, see page 9 here: http://www.cooperativepatentclassification.org/publications/GuideToTheCPC.pdf
    # list of classes in the patent, to see if it is broad or narrow
    classes = []
    for c in patent['cpcs']:
        if cpc['cpc_subsection_id']!=None:
            if c['cpc_subsection_id'] not in classes:
                classes.append(c['cpc_subsection_id'])
    patent['classes'] = classes

# write JSON data to file
with open("clean_patents_info.json", "w") as fp:
    json.dump(patents, fp)
