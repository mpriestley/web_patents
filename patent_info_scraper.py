# this code gathers fulltext descriptions for each patent from the USPTO website

from lxml import html
import requests, json

# open the file that contains the list of patents
# renamed from the "clean_patents_info.json file" ?
# file gets updated repeatedly after every 50 patents 
f=open("patents_fulltext.json","r")
data=f.read()
f.close()
patents=json.loads(data)

# keep track in case something goes wrong
problem_patents = []
# counter
counter = 0

# iterate through patents
for patent in patents:
    if 'description' not in patent:
        number = patent['patent_number']
        counter+=1
        try:
            page = requests.get('http://patft.uspto.gov/netacgi/nph-Parser?Sect2=PTO1&Sect2=HITOFF&p=1&u=/netahtml/PTO/search-bool.html&r=1&f=G&l=50&d=PALL&RefSrch=yes&Query=PN/'+ number)
            tree = html.fromstring(page.content)
            # gather text from document body
            info = str((tree.xpath('/html/body'))[0].text_content())
            # clean up the text a little
            info = info.replace("\n"," ")
            info = info.replace('\"', '')
            patent['description'] = info
            if counter%50==0:
                counter = 0
                # write JSON data to file
                with open("patents_fulltext.json", "w") as fp:
                    json.dump(patents, fp)
        except:
            problem_patents.append(patent)
# write JSON data to file
with open("patents_fulltext.json", "w") as fp:
    json.dump(patents, fp)