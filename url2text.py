from urllib.request import urlopen
from bs4 import BeautifulSoup
import io
import requests
import urllib.request
from pdfminer.high_level import extract_text
import os

# ------- Extracting text from a PDF URL ------------    

url = "https://arxiv.org/pdf/2112.03918.pdf"
r = requests.get(url)
f = io.BytesIO(r.content)
text = extract_text(f)
print(text)

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



