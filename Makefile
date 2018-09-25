PROJECT=cv
all: $(PROJECT).pdf
	

fdiaz.bib: $(PROJECT).tex Makefile clean
	xelatex $(PROJECT).tex
	bibexport -b export.bst -o tmp.bib $(PROJECT).aux
	sed "s/Fernando Diaz/\\\\textcolor{BrickRed}{Fernando Diaz}/g" tmp.bib | sed "s/Diaz, Fernando/\\\\textcolor{BrickRed}{Fernando Diaz}/g" | sed "s/award.*=.*{\(.*\)}/note = {\\\\bf{\1}}/g" > fdiaz.bib
	rm -f tmp.bib

$(PROJECT).pdf: $(PROJECT).tex fdiaz.bib Makefile
	xelatex $(PROJECT).tex
	bibtex $(PROJECT)
	xelatex $(PROJECT).tex
	xelatex $(PROJECT).tex

clean:
	rm -f $(PROJECT).pdf $(PROJECT).aux $(PROJECT).bbl $(PROJECT).blg $(PROJECT).log $(PROJECT).out fdiaz.bib