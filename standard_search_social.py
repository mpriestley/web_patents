# this code looks for W3C standard references in the patent descriptions
import json, re

# standards
standards = {'CGI':r'\b(CGI|(C|c)ommon (G|g)ateway (I|i)nterfaces?)\b',
             'CSS':r'\b(CSS|(C|c)ascading (S|s)tyle (S|s)heets)\b',
             'DOM':r'\b(DOM|(D|d)ocument (O|o)bject (M|m)odel)\b',
             'GRDDL':r'\b(GRDDL|(G|g)leaning (R|r)esource (D|d)escriptions from (D|d)ialects of (L|l)anguages)\b',
             'HTML':r'\b(HTML|(H|h)yper(T|t)ext (M|m)arkup (L|l)anguage)\b',
             'MathML':r'\b((M|m)athML|(M|m)athematical (M|m)arkup (L|l)anguage)\b',
             'OWL':r'\b(OWL|(W|w)eb (O|o)ntology (L|l)anguage)\b',
             'P3P':r'\b(P3P|(P|p)latform for (P|p)rivacy (P|p)references)\b',
             'PROV':r'\b(PROV|(P|p)rovenance)\b',
             'RDF':r'\b(RDF(S|s)?|(R|r)esource (D|d)escription (F|f)ramework)\b',
             'SISR':r'\b(SISR|(S|s)emantic (I|i)nterpretation for (S|s)peech (R|r)ecognition)\b',
             'SKOS':r'\b(SKOS|(S|s)imple (K|k)nowledge (O|o)rganization (S|s)ystem)\b',
             'SMIL':r'\b(SMIL|(S|s)ynchronized (M|m)ultimedia (I|i)ntegration (L|l)anguage)\b',
             'SOAP':r'\b(SOAP|(S|s)imple (O|o)bject (A|a)ccess (P|p)rotocol)\b',
             'SPARQL':r'\bSPARQL\b',
             'SRGS':r'\b(SRGS|(S|s)peech (R|r)ecognition (G|g)rammar (S|s)pecification)\b',
             'SSML':r'\b(SSML|(S|s)peech (S|s)ynthesis (M|m)arkup (L|l)anguage)\b',
             'SVG':r'\b(SVG|(S|s)calable (V|v)ector (G|g)raphics?)\b',
             'VXML':r'\b(VXML|(V|v)oiceXML)\b',
             'XHTML':r'\b(XHTML|(E|e)xtensible (H|h)yper(T|t)ext (M|m)arkup (L|l)anguage)\b',
             'XML':r'\b(XML|(E|e)(X|x)tensible (M|m)arkup (L|l)anguage)\b',
             'XPath':r'\bXPath\b','XQuery':r'\bXQuery\b','XForms':r'\bXForms\b',
             'XSLT':r'\b(XSLT?|(E|e)xtensible (S|s)tylesheet (L|l)anguage)\b',
             'WCAG':r'\b(WCAG|(W|w)eb (C|c)ontent (A|a)ccessibility (G|g)uidelines)\b',
             'WSDL':r'\b(WSDL|(W|w)eb (S|s)ervices (D|d)escription (L|l)anguage)\b',
             # Web 2.0 keywords:
             'RSS':r'\bRSS\b','API':r'\bAPI','mashup':r'\b(M|m)ashup','podcast':r'\b(P|p)odcast',
             'blog':r'\b(B|b)log','tagcloud':r'\b(T|t)agcloud','wiki':r'\b(W|w)iki','permalink':r'\b(P|p)ermalink',
             'network':r'\b(S|s)ocial network'}

# function to check for standard matches in text
def keywordFinder(standards, text):
    # keep a record of standard matches
    matches = []
    if text!=None:
        for standard in standards:
            if re.compile(standards[standard]).search(text)!=None:
                matches.append(standard)
    return matches


# open the file that contains the list of patents
f=open("patents_fulltext.json","r")
patents=f.read()
f.close()
patents=json.loads(patents)

for patent in patents:
    text=patent['description']
    # add any keyword matches, including Web 2.0
    patent['standards'] = keywordFinder(standards, text)
    #print(patent['standards'])

# write JSON data to file
with open("patents_fulltext_standards_social.json", "w") as fp:
    json.dump(patents, fp)
