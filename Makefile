all: index.html

index.html: generatewebpage.py references.csv table1.csv table2.csv ecocyc.csv about.html contribute.html
	./generatewebpage.py

# The final webpage is generated from table1.csv, table2.csv, and references.csv. All these files were themselves originally generated automatically by a bunch of python scripts and bash commands from the raw data extracted from the pdf. However now that only manual corrections are needed it makes more sense to directly modify these 'final' files. They are thus added to the git repository, and are the ones which should be edited. The original and intermediate files are present in the 'history' folder, but are not be used anymore. The history folder also contains the original Makefile used to generate these files.
