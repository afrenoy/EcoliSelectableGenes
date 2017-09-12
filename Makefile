all: larossa.html

larossa.html: references-4.csv table1-4.csv table2-4.csv
	./generatewebpage.py table1-4.csv table2-4.csv references-4.csv larossa.html

clean:
	rm -f table1-2.csv table1-3.csv table2-2.html table2-3.csv references-1.html references-2.html references-3.html references-4.csv table1-4.csv table2-4.csv

table1-4.csv: table1-1.csv
	cat table1-1.csv |sed 's/<i>\([^<]*\)<\/i>/*\1*/g' |sed 's/<b>\([^<]*\)<\/b>/**\1**/g' > table1-2.csv
	cat table1-2.csv |sed 's/;\*\([a-zA-Z]*\)\*$$/;\1/g' > table1-3.csv
	./createtable1.py table1-3.csv > table1-4.csv

table2-4.csv: table2-1.html
	cat table2-1.html |sed 's/<br\/>//g' > table2-2.html
	cat table2-2.html |tr '\n' ';' |sed 's/;<i>\([a-z][a-z][a-z]\)/{<i>\1/g' |tr '{' '\n' > table2-3.csv
	echo "<strong>TABLE 2</strong> Genes for which selections exist in <i>E. coli</i> and <i>S. typhimurium</i>" > table2-4.csv
	echo "Gene;Organism;Selection;References;Alteration" >> table2-4.csv
	cat table2-3.csv |sed 's/^<i>\([a-zA-Z]*\)<\/i>/\1/g' |sed 's/\([;\|,]\)[^;,]*Epelbaum[^;,]*\([;\|,]\)/\1872\2/g' |sed 's/\([;\|,]\)[^;,]*Comai[^;,]*\([;\|,]\)/\1869\2/g' |sed 's/\([;\|,]\)[^;,]*Lin et al[^;,]*\([;\|,]\)/\1870\2/g' |sed 's/\([;\|,]\)[^;,]*Miller[^;,]*\([;\|,]\)/\1871\2/g' |sed 's/\([;\|,]\)[^;,]*Freitag[^;,]*\([;\|,]\)/\1873\2/g' |sed 's/–/-/g' >> table2-4.csv

references-4.csv: references.html supref.txt
	cat references.html|gsed 's/^\(\&\#160;[ ]*\)\+//g' |sed 's/\&\#160;/ /g' > references-1.html
	cat references-1.html |tr '\n' ';' |gsed 's/<br\/>;\([0-9]\{1,3\}[a]\?\.\)/}\1/g' |tr '}' '\n' > references-2.html
	cat references-2.html |sed 's/;//g' |sed 's/<br\/>/ /g' |sed 's/$$/<br\/>/g' > references-3.html
	cat references-3.html|sed 's/<\/b> *<b>/ /g' |gsed 's/^\([0-9]*[a]\?\)\. *<b>\([a-zA-Z ,\.’èöé-]*\)\.<\/b> *\([0-9]*\)\(.*\)<i>\([a-zA-Z \.:,é-]*\)<\/i>\( *<b>\|[^<]*<br\)/\1;\2;\3;\4;\5\6/g' |sed 's/<br\/>//g' > references-4.csv
	cat supref.txt >> references-4.csv

