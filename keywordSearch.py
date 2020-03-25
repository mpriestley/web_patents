# this code goes through all the patents and creates a file
# containing only those that satisfy the keyword condition
# requires patent.json and application.json file
# returns relevant_patents.json, relevant_patents.csv and patents_by_month.csv
# runtime is a couple of hours

import json, csv, re

# KEYWORDS ######################################
# each keyword is written as a regular expression
# letter case is important (e.g. "SOAP" is different to "soap")
main_key = r'(?i)\bworld wide web\b'
# keywords: HTTP, HTTPS, WebSocket, WebDAV
keys = [r'\bHTTP\b',r'\bHTTPS\b',r'\b(W|w)eb(S|s)ockets?\b',r'\b((W|w)ebDAV|(W|w)eb (D|d)istributed (A|a)uthoring and (V|v)ersioning)\b', 
        # URL, URI,
        r'\b(URLs?|(U|u)niform (R|r)esource (L|l)ocators?)\b',r'\b(URIs?|(U|u)niform (R|r)esource (I|i)dentifiers?)\b', 
        # hyper(text|link|media), browser, (internet|TCP/IP|online|server(s)),
        r'\b(H|h)yper(text|links?|media)\b', r'\b(B|b)rowsers?\b', r'\b((I|i)nternet|TCP/IP|(O|o)nline|(S|s)ervers?)\b',
        # web(site(s)), wiki(s), blog, rss
        r'\b(W|w)eb(sites?)?\b', r'\b(W|w)ikis?\b', r'\b(B|b)log', r'\b(RSS|(R|r)eally (S|s)imple (S|s)yndication|(R|r)ich (S|s)ite (S|s)ummary)\b',
        # WAP, WML
        r'\b(WAPs?|(W|w)ireless (A|a)pplication (P|p)rotocols?)\b',r'\b(WML|(W|w)ireless (M|m)arkup (L|l)anguage)\b',
        # CGI, WSDL
        r'\b(CGI|(C|c)ommon (G|g)ateway (I|i)nterfaces?)\b',r'\b(WSDL|(W|w)eb (S|s)ervices (D|d)escription (L|l)anguage)\b',
        # UDDI
        r'\b(UDDI|(U|u)niversal (D|d)escription,? (D|d)iscovery and (I|i)ntegration)\b',
        # servlet, applet, SOAP
        r'\b(S|s)ervlets?\b',r'\b(A|a)pplets?\b',r'\b(SOAP|(S|s)imple (O|o)bject (A|a)ccess (P|p)rotocol)\b',
        # REST, webRTC
        r'\b(REST|(R|r)(E|e)presentational (S|s)tate (T|t)ransfer)\b',r'\b((W|w)ebRTC|(W|w)eb (R|r)eal( |-)(T|t)ime (C|c)ommunication)\b',
        # P3P, WCAG
        r'\b(P3P|(P|p)latform for (P|p)rivacy (P|p)references)\b', r'\b(WCAG|(W|w)eb (C|c)ontent (A|a)ccessibility (G|g)uidelines)\b',
        # HTML, XHTML
        r'\b(HTML|(H|h)yper(T|t)ext (M|m)arkup (L|l)anguage)\b',r'\b(XHTML|(E|e)xtensible (H|h)yper(T|t)ext (M|m)arkup (L|l)anguage)\b',
        # HTML5, CSS, JavaScript
        r'\bHTML5\b',r'\b(CSS|(C|c)ascading (S|s)tyle (S|s)heets)\b', r'(?i)\bJavaScript\b',
        # DOM, XML
        r'\b(DOM|(D|d)ocument (O|o)bject (M|m)odel)\b', r'\b(XML|(E|e)(X|x)tensible (M|m)arkup (L|l)anguage)\b',
        # VoiceXML, SISR
        r'\b(VXML|(V|v)oiceXML)\b', r'\b(SISR|(S|s)emantic (I|i)nterpretation for (S|s)peech (R|r)ecognition)\b',
        # SRGS, SMIL
        r'\b(SRGS|(S|s)peech (R|r)ecognition (G|g)rammar (S|s)pecification)\b',  r'\b(SMIL|(S|s)ynchronized (M|m)ultimedia (I|i)ntegration (L|l)anguage)\b',
        # XSL, XPath, XQuery, XForms
        r'\b(XSLT?|(E|e)xtensible (S|s)tylesheet (L|l)anguage)\b',r'\bXPath\b',r'\bXQuery\b',r'\bXForms\b',
        # JSON, SVG, PNG
        r'\b(JSON|(J|j)ava(S|s)cript (O|o)bject (N|n)otation)\b',r'\b(SVG|(S|s)calable (V|v)ector (G|g)raphics?)\b',r'\b(PNG|(P|p)ortable (N|n)etwork (G|g)raphics?)\b',
        # SSML, MathML,
        r'\b(SSML|(S|s)peech (S|s)ynthesis (M|m)arkup (L|l)anguage)\b',r'\b((M|m)athML|(M|m)athematical (M|m)arkup (L|l)anguage)\b',
        # AJAX, CCPP
        r'(?i)\b(AJAX|Asynchronous JavaScript and XML)\b',r'\b(CC/PP|(C|c)omposite (C|c)apability (P|p)reference (P|p)rofiles)\b',
        # RDF, SPARQL
        r'\b(RDF(S|s)?|(R|r)esource (D|d)escription (F|f)ramework)\b',r'\bSPARQL\b',
        # OWL, SKOS
        r'\b(OWL|(W|w)eb (O|o)ntology (L|l)anguage)\b', r'\b(SKOS|(S|s)imple (K|k)nowledge (O|o)rganization (S|s)ystem)\b',
        # GRDDL, PROV
        r'\b(GRDDL|(G|g)leaning (R|r)esource (D|d)escriptions from (D|d)ialects of (L|l)anguages)\b', r'\b(PROV|(P|p)rovenance)\b',]

#store relevant patents
rel_patents={}
rel_patents['patents']=[]

# function to check for keyword matches in text
def keywordFinder(main_key, keys, text):
    if text!=None:
        # check for main keyword
        if re.compile(main_key).search(text)!=None:
            return True
        # keep a record of other keyword matches
        matches = 0
        for keyword in keys:
            if re.compile(keyword).search(text)!=None:
                matches+=1
            if matches > 1:
                # if there is more than one match, return true
                return True
    return False


#open the file that contains the list of patents
f=open("patent.json","r")
patents=f.read()
f.close()
patents=json.loads(patents)['data']

#open the file that contains the list of patent application dates
f=open("application.json","r")
apps=f.read()
f.close()
apps=json.loads(apps)['data']
# transform these into a dict of patent numbers and app dates
app_dates = {}
for app in range(0,len(apps)):
    number = apps[app]['patent_id']
    app_dates[number] = apps[app]['date']

# dict to store the date and patent frequencies
new_patents={}

problem_patents = [] # to keep track of any that go wrong

# record application and grant dates for all patents, as well as web-related patents only
# this is so that we can keep track of the proportion of web-related patents
for patent in patents:
    number = patent['number']
    gr_date = patent['date']
    year_month = re.split("-", gr_date)
    gr_date="01/"+year_month[1]+"/"+year_month[0] #all days of the month are set to 1 (first day of the month) for consistency and ease of use
    try:
        app_date = app_dates[number]
        year_month = re.split("-", app_date)
        app_date="01/"+year_month[1]+"/"+year_month[0]
        if gr_date not in new_patents:
            new_patents[gr_date]={"tot_patents_gr":1, "web_patents_gr":0,"tot_patents_ap":0, "web_patents_ap":0}
        else:
            new_patents[gr_date]['tot_patents_gr']+=1
        if app_date not in new_patents:
            new_patents[app_date]={"tot_patents_gr":0, "web_patents_gr":0,"tot_patents_ap":1, "web_patents_ap":0}
        else:
            new_patents[app_date]['tot_patents_ap']+=1
        abstract=patent['abstract']
        title=patent['title']
        # combine patent title and abtract into one block of text
        text = title + ' '+ abstract
        # look for keyword matches
        if keywordFinder(main_key, keys, text)==True:
            rel_patents['patents'].append(patent)
            new_patents[app_date]['web_patents_ap']+=1
            new_patents[gr_date]['web_patents_gr']+=1
    except:
        problem_patents.append(patent)

# write JSON data to file
with open('relevant_patents.json', 'w') as f:
    json.dump(rel_patents, f)
# make a simpler version in csv format for manual inspection (checking precision)
with open('relevant_patents.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for patent in rel_patents['patents']:
        writer.writerow([patent['title'],patent['abstract'], patent['number']])
print(len(rel_patents['patents']))


# after manual examination, exclude irrelevant patents from monthly counts
# irrelevant patent numbers
irrel = ['5544320','5570084','5696901','5745753','5935637','5958137','5980442','7247391',
         '7261217','9096973','5974444','6312523','6470446','6497383','7497399','8113377',
         '8317054','8635352','9220297','9432813','6536705','6588866','6799083','6875308',
         '6908531','7021482','7114627','7462259']
for pat in irrel:
    date = app_dates[pat]
    year_month = re.split("-", date)
    date="01/"+year_month[1]+"/"+year_month[0]
    new_patents[date]['web_patents_ap']-=1
    for patent in rel_patents['patents']:
        if patent['number'] == pat:
            gr_date = patent['date']
            year_month = re.split("-", gr_date)
            gr_date="01/"+year_month[1]+"/"+year_month[0] #all days of the month are set to 1 (first day of the month) for consistency and ease of use
            new_patents[gr_date]['web_patents_gr']-=1


with open('patents_by_month.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    # Write CSV Header
    writer.writerow(["DATE", "tot_patents_ap", "web_patents_ap", "tot_patents_gr", "web_patents_gr"])
    for x in range(0,len(new_patents)):
        writer.writerow([list(new_patents.keys())[x],  # app date
                    new_patents[list(new_patents.keys())[x]]['tot_patents_ap'],
                    new_patents[list(new_patents.keys())[x]]['web_patents_ap'],
                    new_patents[list(new_patents.keys())[x]]['tot_patents_gr'],
                    new_patents[list(new_patents.keys())[x]]['web_patents_gr']]) # patents