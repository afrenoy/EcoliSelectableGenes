all: index.html

index.html: generatewebpage.py references.csv table1.csv table2.csv ecocyc.csv about.html contribute.html
	./generatewebpage.py

# The final webpage is generated from table1.csv, table2.csv, and references.csv. All these files were themselves originally generated automatically by a bunch of python scripts and bash commands from the raw data extracted from the pdf. However now that only manual corrections are needed it makes more sense to directly modify these 'final' files. They are thus added to the git repository, and are the ones which should be edited. The other intermediate files should not be used anymore, and the commands below will not be used anymore.

clean:
	rm -f table1-2.csv table1-3.csv table2-2.html table2-3.csv references-1.html references-2.html references-3.html

table1.csv: table1-1.csv
	cat table1-1.csv |sed 's/<i>\([^<]*\)<\/i>/*\1*/g' |sed 's/<b>\([^<]*\)<\/b>/**\1**/g' > table1-2.csv
	cat table1-2.csv |sed 's/;\*\([a-zA-Z]*\)\*$$/;\1/g' > table1-3.csv
	./createtable1.py table1-3.csv > table1.csv

table2.csv: table2-1.html
	cat table2-1.html |sed 's/<br\/>//g' > table2-2.html
	cat table2-2.html |tr '\n' ';' |sed 's/;<i>\([a-z][a-z][a-z]\)/{<i>\1/g' |tr '{' '\n' > table2-3.csv
	echo "Genes for which selections exist in <i>E. coli</i> and <i>S. typhimurium</i>" > table2.csv
	echo "Gene;Organism;Selection;References;Alteration" >> table2.csv
	cat table2-3.csv |sed 's/^<i>\([a-zA-Z]*\)<\/i>/\1/g' |sed 's/\([;\|,]\)[^;,]*Epelbaum[^;,]*\([;\|,]\)/\1872\2/g' |sed 's/\([;\|,]\)[^;,]*Comai[^;,]*\([;\|,]\)/\1869\2/g' |sed 's/\([;\|,]\)[^;,]*Lin et al[^;,]*\([;\|,]\)/\1870\2/g' |sed 's/\([;\|,]\)[^;,]*Miller[^;,]*\([;\|,]\)/\1871\2/g' |sed 's/\([;\|,]\)[^;,]*Freitag[^;,]*\([;\|,]\)/\1873\2/g' |sed 's/–/-/g' >> table2.csv

references.csv: references.html supref.txt
	cat references.html|gsed 's/^\(\&\#160;[ ]*\)\+//g' |sed 's/\&\#160;/ /g' > references-1.html
	cat references-1.html |tr '\n' ';' |gsed 's/<br\/>;\([0-9]\{1,3\}[a]\?\.\)/}\1/g' |tr '}' '\n' > references-2.html
	cat references-2.html |sed 's/;//g' |sed 's/<br\/>/ /g' |sed 's/$$/<br\/>/g' > references-3.html
	cat references-3.html|sed 's/<\/b> *<b>/ /g' |gsed 's/^\([0-9]*[a]\?\)\. *<b>\([a-zA-Z ,\.’èöé-]*\)\.<\/b> *\([0-9]*\)\(.*\)<i>\([a-zA-Z \.:,é-]*\)<\/i>\( *<b>\|[^<]*<br\)/\1;\2;\3;\4;\5\6/g' |sed 's/<br\/>//g' |sed 's/<b>//g' |sed 's/<\/b>//g' > references.csv
	cat supref.txt >> references.csv

