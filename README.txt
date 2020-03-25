This repository contains Python scripts for gathering and cleaning the dataset of Web-related patents.
Corresponding author:
Maria Priestley (mp5g15@soton.ac.uk) – Web and Internet Science Group, University of Southampton

For additional detail about the dataset and how it was processed, please refer to the document 'dataset_description.pdf'.

This project is licensed under the terms of the cc-by-4.0 license.

Contents of this repository (in order of execution):

patent.json			# bulk dataset of all US patents granted since 1976
application.json		# data containing application dates, which aren't included in the bulk patent file
keywordSearch.py		# keyword filtering rule implementation to select Web-related patents only (uses 'patent.json' as input, produces 'relevant_patents.json', 'relevant_patents.csv' and 'patents_by_month.csv' as output)
relevant_patents.json		# basic data on Web-related patents
relevant_patents.csv		# basic descriptions of Web-related patents (used for manual relevance checking)
patents_by_month.csv		# monthly patenting variables (Web patent apps, total patent apps etc.)
patentHarvester.py		# uses PatentsView API to gather additional data attributes for each relevant patent (uses 'relevant_patents.json' as input and produces 'relevant_patents_info.json')
relevant_patents_info.json 	# detailed attributes for relevant patents
patentSampleCleaner.py		# cleans and sorts the data, and adds some new variables (uses 'relevant_patents_info.json' as input and produces 'clean_patents_info.json')
clean_patents_info.json		# patent dataset ready for the extraction of variables
recall_test.py 			# evaluates the recall of the keyword filtering rule
rand_sample_annotated.json	# manually checked sample for recall calculation
(the following data-processing operations were applied for the purposes of a Web standards diffusion project)
patent_info_scraper.py 		# gathers fulltext descriptions for each patent from the USPTO website
				(creates 'patents_fulltext.json' from a data template, built from 'clean_patents_info.json'?)
patents_fulltext.json		# patent dataset with full text descriptions
standard_search_social.py	# looks for W3C standards and Web 2.0 keywords in the patent descriptions 
				(uses 'patents_fulltext.json' and creates 'patents_fulltext_standards_social.json')
patents_fulltext_standards_social.json # patent dataset with a new variable containing a list of featured W3C standards and Web 2.0 keywords
assignee_cleaner.py		# identifies misspelled or duplicate assignee names using similarity matching (uses 
				'patents_fulltext_standards_social.json' and 'company_aliases_manual.csv' as input, gives 'company_aliases.csv' and 'patents_final.json' as output)
company_aliases.csv		# list of similar assignee names produced by algorithm
company_aliases_manual.csv	# manually edited list of assignees specifying the changes required
patents_final.json 		# patent dataset with cleaned assignee names