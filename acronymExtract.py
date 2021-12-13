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
    url = "https://arxiv.org/pdf/2110.11694"
    text = file_read(url)
    # print(text)
    # acronym_list = set([x.group() for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text)])
    # print(acronym_list)
    for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text):
        print(x.group(), x.start(), x.end())

def window_range(startidx, endidx, size):
    if(startidx < size)

def play():
    fpath =  "play.txt"
    with open(fpath,'r') as f:
        text_file = f.readlines()
        text_file = ' '.join(text_file)
        text_file = re.sub(r"[^A-Za-z\.&]", " ", text_file)
        text_file = ' '.join(text_file)
        
        for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text):
            ## Routine to build a window 
            ## Search for expansion
            ## Add to dictionary


    print(text_file)
    

play()