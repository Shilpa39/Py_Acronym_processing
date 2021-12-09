import PyPDF2 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import io
import requests
import urllib.request
from pathlib import Path

# ------- Extracting text from a PDF file existing locally ------------    

# creating a pdf file object 
pdfFileObj = open('PDF_dataset/pdf2.pdf', 'rb') 
    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
   
text = ""
for i in range(pdfReader.numPages):
    # creating a page object  
    pageObj = pdfReader.getPage(i) 
    # extracting text from page
    text = text + pageObj.extractText()

"""with open("output1.txt",'w') as o1:
  o1.write(text)"""
print(text) 
    
# closing the pdf file object 
pdfFileObj.close()

# ------- Extracting text from a HTML URL ------------    
url = "http://kite.com"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text2 = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text2.splitlines())

# drop blank lines
text2 = ' '.join(line for line in lines if line)

print(text2)

# ------- Extracting text from a PDF URL ------------    

#url2 = 'http://ceur-ws.org/Vol-2150/BARR2_paper2.pdf'
#url2 = "http://www.africau.edu/images/default/sample.pdf"
url2 = "https://arxiv.org/pdf/2112.03918.pdf"
r = requests.get(url2)
 
# the HTTP response in a response object called r
with open("filename2.pdf",'wb') as fi:
  
    # Saving received content as a png file in
    # binary format
  
    # write the contents of the response (r.content)
    # to a new file in binary mode.
    fi.write(r.content)

# creating a pdf file object 
pdfFileObj2 = open('filename2.pdf', 'rb') 
    
# creating a pdf reader object 
pdfReader2 = PyPDF2.PdfFileReader(pdfFileObj2) 
   
text3 = ""
for i in range(pdfReader2.numPages):
    # creating a page object  
    pageObj2 = pdfReader2.getPage(i) 
    # extracting text from page
    pagetext = pageObj2.extractText()
    text3 = text3 + pagetext


"""with open("output2.txt",'w') as o2:
  o2.write(text3)"""
print(text3)    
print("\n ---------------------------------------------------------------- \n")


