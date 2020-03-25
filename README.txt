This repository contains Python scripts for gathering and cleaning the dataset of Web-related patents.
Corresponding author:
Maria Priestley (mp5g15@soton.ac.uk) – Web and Internet Science Group, University of Southampton

For additional detail about the dataset and how it was processed, please refer to the document 'dataset_description.pdf'.

This project is licensed under the terms of the cc-by-4.0 license.

Contents of this repository (in order of execution):

keywordSearch.py		# keyword filtering rule implementation to select Web-related patents only (uses 'patent.json' as input, produces 'relevant_patents.json', 'relevant_patents.csv' and 'patents_by_month.csv' as output)
patentHarvester.py		# uses PatentsView API to gather additional data attributes for each relevant patent (uses 'relevant_patents.json' as input and produces 'relevant_patents_info.json')
patentSampleCleaner.py		# cleans and sorts the data, and adds some new variables (uses 'relevant_patents_info.json' as input and produces 'clean_patents_info.json')
recall_test.py 			# evaluates the recall of the keyword filtering rule
patent_info_scraper.py 		# gathers fulltext descriptions for each patent from the USPTO website
				(creates 'patents_fulltext.json' from a data template, built from 'clean_patents_info.json'?)
standard_search_social.py	# looks for W3C standards and Web 2.0 keywords in the patent descriptions 
				(uses 'patents_fulltext.json' and creates 'patents_fulltext_standards_social.json')
assignee_cleaner.py		# identifies misspelled or duplicate assignee names using similarity matching (uses 
				'patents_fulltext_standards_social.json' and 'company_aliases_manual.csv' as input, gives 'company_aliases.csv' and 'patents_final.json' as output)
