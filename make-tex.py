#!/usr/bin/env python3

import sys
import json
import argparse

def printHeader():
    with open("cv-header.tex","r") as fp:
        print(fp.read())
def printSummary(X):
    print("\\section{Summary}\\noindent")
    print("%s\\\\\n"%(X))

def printDegrees(X):
    print("\\section{Education}\\noindent\\begin{tabbing}")
    print("\\hspace{4em}\= \\kill")
    isFirst = True
    for x in X:
        if not isFirst:
            print("\\\\")
        print("%s\\>\\textbf{%s}\\` %s\\\\"%(x["degree"],x["school"],x["year"]))
        print("\\>%s\\\\"%(x["discipline"]))
        if "thesis" in x:
            print("\\>\\emph{``%s''}\\\\"%(x["thesis"]))
            print("\\>%s\\\\"%(", ".join(x["readers"])))
        isFirst = False
    print("\\end{tabbing}\n\n")
    
            
def printAcademicAffiliations(X):
    print("\\section{Academic \\\\Affiliation}\\noindent")
    for x in X:
        s = "%s %d"%(x["start-month"],x["start-year"])
        if not("end-year" in x):
            e="present"
        else:
            e = "%s %d"%(x["end-month"],x["end-year"])
        if "description" in x:
            print("\\noindent\\textbf{%s}\\hfill %s\\\\%s\\hfill %s-%s\\\\\\\\\n%s\\\\\n"%(x["school"],x["title"],x["location"],s,e,x["description"]))
        else:
            print("\\textbf{%s}\\hfill %s\\\\%s\\hfill %s-%s\\\\\\\\"%(x["school"],x["title"],x["location"],s,e))
    print("\n\n")

def printEmployment(X):
    print("\\section{Positions}")
    for x in X:
        s = "%s %d"%(x["start-month"],x["start-year"])
        if not("end-year" in x):
            e="present"
        else:
            e = "%s %d"%(x["end-month"],x["end-year"])
        title="\\noindent\\textbf{%s}\\hfill %s\\\\\n%s\\hfill %s-%s\\\\\n"%(x["affiliation"],x["title"],x["location"],s,e)
        if "relocation" in x:
            ss = "%s %d"%(x["relocation-start-month"],x["relocation-start-year"])
            if not("relocation-end-year" in x):
                ee="present"
            else:
                ee = "%s %d"%(x["relocation-end-month"],x["relocation-end-year"])
            title+="%s\\hfill %s-%s\\\\"%(x["relocation"],ss,ee)
        else:
            title+=""
        print(title+"\\\\%s\\\\\n"%(x["description"]))
    print("\n\n")

def printTeaching(X):
    # print("\\section{Academic \\\\Teaching}")
    print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Academic}\\\\\\\\")
    for x in X:
        print("\\noindent\\textbf{%s} \\\\\n%s\\hfill %s\\\\\\\\\n%s\\\\\n"%(x["title"],x["school"],", ".join(x["semesters"]),x["description"]))
    print("\n\n")
def printTutorials(X):
    if "tutorials" in X:
        # print("\\section{Tutorials}\\noindent")
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Tutorials}\\\\")
        for x in X["tutorials"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)

def printSupervision(X):
    print("\\section{Supervision}")
    if "interns" in X:
        print("\\noindent\\textbf{Former Interns}\\\\")
        sortedInterns = sorted(X["interns"],key=lambda x: x["year"], reverse=True)
        for x in sortedInterns:
            print("%s (%s), %s, %s\\\\"%(x["name"],", ".join(map(lambda y:"%d"%y, x["year"])),x["title"],x["affiliation"]))
        print("\n\n")
    if "reader" in X:
        print("\\noindent\\textbf{PhD Examiner}\\\\")
        sortedStudents = sorted(X["reader"],key=lambda x: x["year"], reverse=True)
        for x in sortedStudents:
            print("%s, %s, %d\\\\"%(x["name"],x["school"],x["year"]))
        print("\n\n")

def printPublications(X,Y, under_review=False):
    print("\\setlength{\\leftmargini}{0em}")
    print("\\section{Publications}")
    
    printBibliometrics(X)
    printBibliography(Y,under_review)
    
def printBibliometrics(X):
    print("\\noindent\\textbf{Metrics}\\\\")
    header = "\\noindent\\begin{center}\\begin{tabular}{l"
    urls=""
    articles = "articles"
    h = "h-index"
    citations = "citations"
    citationsPerArticle = "citations/article"
    for src in ["acm","scopus","google-scholar","allen","aminer"]:
        header+="C{0.5in}"
        urls += " & "
        articles += " & "
        h += " & "
        citations += " & "
        citationsPerArticle += " & "
        if src=="acm":
            urls += "\\href{http://dl.acm.org/author\\_page.cfm?id=%s}{\\textit{{ACM DL}}}"%(X[src]["id"])
        elif src=="scopus":
            urls += "\\href{https://www.scopus.com/authid/detail.uri?authorId=%s}{\\textit{{Scopus}}}"%(X[src]["id"])
        elif src=="google-scholar":
            urls += "\\href{http://scholar.google.com/citations?user=%s}{\\textit{{Google Scholar}}}"%(X[src]["id"])
        elif src=="allen":
            urls += "\\href{https://www.semanticscholar.org/author/%s}{\\textit{{Semantic Scholar}}}"%(X[src]["id"])
        elif src=="aminer":
            urls += "\\href{https://www.aminer.org/profile/%s}{\\textit{{AMiner}}}"%(X[src]["id"])
        articles += "%d"%X[src]["articles"]
        citations += "%d"%X[src]["citations"]
        citationsPerArticle += "%.1f"%(X[src]["citations"]/X[src]["articles"])
        h += "%d"%X[src]["h"]
    print("%s}"%header)
    print("%s\\\\"%urls)
    print("\\hline")
    print("%s\\\\"%articles)
    print("%s\\\\"%citations)
    print("%s\\\\"%citationsPerArticle)
    print("%s\\\\"%h)
    print("\\end{tabular}\n\\end{center}")
    # print("\\noindent\\begin{center}\\begin{tabular}{lccc}&\\href{http://dl.acm.org/author\\_page.cfm?id=%s}{\\textit{ACM Digital Library}}&\\href{https://www.scopus.com/authid/detail.uri?authorId=%s}{\\textit{Scopus}}&\\href{http://scholar.google.com/citations?user=%s}{\\textit{Google Scholar}}\\\\\n\\hline\narticles&&&\\\\\ncitations&&&\\\\\ncitations/article&&&\\\\\nh-index&&&\n\\end{tabular}\n\\end{center}"%(X["acm"],X["scopus"],X["google-scholar"]))
    
def printBibliography(X,under_review=False):
    if (under_review is True) and ("under-review" in X) and (len(X["under-review"]) > 0):
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Under Review}\\\\")
        for x in X["under-review"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "conference-papers" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Conference Papers}\\\\")
        for x in X["conference-papers"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "journal-articles" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Journal Articles}\\\\")
        for x in X["journal-articles"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "book-chapters" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Chapters}\\\\")
        for x in X["book-chapters"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "books" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Books}\\\\")
        for x in X["books"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "theses" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Thesis}\\\\")
        for x in X["theses"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "workshop-papers" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Workshop Papers}\\\\")
        for x in X["workshop-papers"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    # if "tutorials" in X:
    #     print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Tutorials}\\\\")
    #     for x in X["tutorials"]:
    #         print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    
def printPatents(X):
    print("\\section{Patents}")
    if "granted" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Granted}\\\\")
        for x in X["granted"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)
    if "applied" in X:
        print("\\vspace{\\baselineskip}\n\\noindent\\textbf{Applied}\\\\")
        for x in X["applied"]:
            print("\\begin{verse}\n\\bibentry{%s}\n\\end{verse}"%x)

def printRecognition(X,Y):
    print("\\section{Recognition}")
    if (X!=None):
        print("\\noindent\\textbf{Awards}\\\\")
        for x in X:
            print("%s, %d\\\\"%(x["title"],x["year"]))
        print("\n\n")
        
    if (Y!=None):
        print("\\noindent\\textbf{Fellowships and Chairs}\\\\")
        for y in Y:
            print("%s, %d\\\\"%(y["title"],y["year"]))

    print("\n\n")

def sequenceToRanges(a):
    retval = ""
    for i in range(len(a)):
        if (i>0):
            if (a[i]-a[i-1])==1:
                if (retval[-1]!="-"):
                    retval="%s-"%retval
            else:
                if retval[-1]=="-":
                    retval="%s%d"%(retval,a[i-1])
                retval="%s, %d"%(retval,a[i])
        else:
            retval="%d"%a[i]
    if (retval[-1]=="-"):
        retval = "%s%d"%(retval,a[-1])
    return retval
    
    
def printService(X):
    print("\\section{Service}")
    if "organizational leadership" in X:
        print("\\noindent\\textbf{Organizational Leadership}\\\\")
        for x in X["organizational leadership"]:
            years = sequenceToRanges(x["year"])
            print("%s, %s, %s\\\\"%(x["venue"],x["title"],years))
            # print("\\\\".join([x["venue"],x["title"],years]))
            # print("\\noindent %s\\hfill %s\\\\"%(x["venue"],x["title"]))
            # print("\\hfill %s\\\\\\"%years)
        print("\n\n")
    if "organizational support" in X:
        print("\\noindent\\textbf{Organizational Support}\\\\")
        for x in X["organizational support"]:
            s = "%d"%(x["start-year"])
            if not("end-year" in x):
                e="present"
            else:
                e = "%d"%(x["end-year"])
            years="%s-%s"%(s,e)
            print("%s, %s, %s\\\\"%(x["venue"],x["title"],years))
        print("\n\n")
    if "technical expertise" in X:
        print("\\noindent\\textbf{Technical Expertise}\\\\")
        for x in X["technical expertise"]:
            years = sequenceToRanges(x["year"])
            print("%s, %s, %s\\\\"%(x["venue"],x["title"],years))
    print("\n\n")
                    
def printSkills(X):
    print("\\section{Skills}\\noindent %s"%(" ".join(X)))
    print("\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--under_review", action=argparse.BooleanOptionalAction, help="include papers under review")
    parser.add_argument("--references", action=argparse.BooleanOptionalAction, help="include references")
    parser.add_argument('input', nargs='*', help='path to cv json file')
    args = parser.parse_args()


    with open(args.input[0],"r") as fp:
        data = json.load(fp)
        printHeader()
        name = " ".join([data["given-name"],data["sur-name"]])
        print("\\author{\\textcolor{BrickRed}{%s}}"%name)
        # print("\\authoremail{%s}"%data["email"])
        # print("\\authorwww{%s}"%data["www"])
        print("\\newcommand{\\authoremail}[0]{%s}"%data["email"])
        print("\\newcommand{\\authorwww}[0]{%s}"%data["www"])
        print("\\begin{document}\n\\maketitle")
        if "summary" in data:
            printSummary(data["summary"])
        if "degrees" in data:
            printDegrees(data["degrees"])
        if "employment" in data:
            printEmployment(data["employment"])
        if "academic-affiliation" in data:
            printAcademicAffiliations(data["academic-affiliation"])
        printPublications(data["bibliometrics"],data["bibliography"],args.under_review)
        if ("teaching" in data) or ("tutorials" in data["bibliography"]):
            print("\\section{Teaching}")
            if ("teaching" in data):
                printTeaching(data["teaching"])
            printTutorials(data["bibliography"])
        if "supervision" in data:
            printSupervision(data["supervision"])
        if "patents" in data:
            printPatents(data["patents"])
        print("\\vspace{1em}")
        if "awards" in data:
            printRecognition(data["awards"],data["fellowships"])
        if "service" in data:
            printService(data["service"])
        if "skills" in data:
            printSkills(data["skills"])
        if not("references" in data):
            print("\\section{References}\\noindent \\emph{Available on request.}")
        print("\\bibliographystyle{plain}")
        print("\\nobibliography{%s}\n\\end{document}"%data["bib"])
        with open("tmp.sed","w") as sfp:
            gs = name
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(gs,name))
            gis = ", ".join([data["given-name"][0],data["sur-name"]])        
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(gis,name))
            gis = ", ".join([data["given-name"][0]+".",data["sur-name"]])        
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(gis,name))
            sg = ", ".join([data["sur-name"],data["given-name"]])        
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(sg,name))
            sgi = ", ".join([data["sur-name"],data["given-name"][0]])        
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(sgi,name))
            sgi = ", ".join([data["sur-name"],data["given-name"][0]+"."])        
            sfp.write("s/%s/\\\\textcolor{BrickRed}{%s}/g\n"%(sgi,name))

if __name__ == "__main__":
    main()
