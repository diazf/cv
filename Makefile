PROJECT=cv
BIB=fdiaz
all: $(PROJECT).pdf
	

$(BIB).bib: $(PROJECT).tex Makefile clean-some
	xelatex $(PROJECT).tex
	bibexport -b export.bst -o tmp.bib $(PROJECT).aux
	sed -f tmp.sed tmp.bib | sed "s/award.*=.*{\(.*\)}/note = {\\\\bf{\1}}/g" > $(BIB).bib
	rm -f tmp.bib tmp.sed	

$(PROJECT).tex: ${PROJECT}.json Makefile
	./make-tex.py ${PROJECT}.json > $(PROJECT).tex

$(PROJECT).pdf: $(PROJECT).tex $(BIB).bib Makefile
	xelatex $(PROJECT).tex
	bibtex $(PROJECT)
	xelatex $(PROJECT).tex
	xelatex $(PROJECT).tex

clean-some:
	rm -f $(PROJECT).pdf $(PROJECT).aux $(PROJECT).bbl $(PROJECT).blg $(PROJECT).log $(PROJECT).out $(BIB).bib 

clean: clean-some
	rm -f $(PROJECT).pdf $(PROJECT).aux $(PROJECT).bbl $(PROJECT).blg $(PROJECT).log $(PROJECT).out $(BIB).bib  $(PROJECT).tex