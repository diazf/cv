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

### Edit `cv.json`

Replace `cv.json` with your CV information.  

The value for `bib` should be basename of the BibTeX library that includes all of your citations.  My current setup has this file in some other directory, assuming you, like I, have a big BibTeX file that happens to contain your own bibliography in addition to everything else.  Make sure this file is in your `BIBINPUTS` environment variable.  
You should not store this in the same directory that you build your CV.

The `bibliography` section of your JSON file should just be a lists of the citation keys in your BibTeX library.  Within each bibliographic section, citations will preserve the order in the JSON file.  

### Edit `Makefile`

Replace `BIB` definition with the basename of the BibTex library. It should be same as in the previous section.

### Run `make`

Build the CV in the same directory as `Makefile` and everything else.  Your CV will be in `cv.pdf`.

## Notes

I've tried to include checks in case you don't want some of the sections I have.

