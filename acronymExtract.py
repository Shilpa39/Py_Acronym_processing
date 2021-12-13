import io
import requests
import re
from pdfminer.high_level import extract_text

# ------- Extracting text from a PDF URL ------------    

def file_read(url):
    r = requests.get(url)
    f = io.BytesIO(r.content)
    text = extract_text(f)
    # print(text)
    return text

def main():
    url = "https://arxiv.org/pdf/2111.00944"
    text = file_read(url)
    # print(text)
    acronym_list = set([x.group() for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text)])
    print(acronym_list)

main()