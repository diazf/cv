# Curriculum Vitae
![cv image](https://github.com/diazf/cv/raw/master/cv.png)

Package to render CV. 

## Dependencies
* [xetex](https://tug.org/xetex/)
* [sed](https://www.gnu.org/software/sed/)
* [bibtex](http://www.bibtex.org)
* [bibexport](https://ctan.org/pkg/bibexport)
* [python3](https://www.python.org/download/releases/3.0/)
* [make](https://www.gnu.org/software/make/)
* and a bunch of latex packages

## Instructions

Replace `cv.json` with your CV information.  

The value for `bib` should be basename of the BibTeX library that includes all of your citations.  Your bibliography should just be a lists of the citation keys in your BibTeX library.  Within each bibliographic section, citations will preserve the order in the JSON file.  

I've tried to include checks in case you don't want some of the sections I have.

