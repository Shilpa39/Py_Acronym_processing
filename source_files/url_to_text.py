import requests
import mimetypes
import magic
import pathlib
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup
import io
import urllib.request
from pdfminer.high_level import extract_text
import os
import re


#user-defined variables - could be overridden by command line arguments
#user_url="https://raw.githubusercontent.com/mathmanu/caffe-jacinto-models/caffe-0.17/trained/image_classification/imagenet_jacintonet11v2/initial/test.prototxt"
#user_url="https://en.wikipedia.org/wiki/Baahubali_2:_The_Conclusion"
user_url="https://arxiv.org/pdf/2110.11694"
isLocal=False;

#user_url="/home/a0492783/Downloads/TI_C7X_DSP_TRAINING_00.06/c7x_dsp_isa/C7x_ISA_Database.html"
#user_url="/home/a0492783/Py_Acronym_processing/testcases/testcases_rawfiles/testcase1.pdf"
user_url="/home/a0492783/Py_Acronym_processing/play.txt"
isLocal=True;

#code starts here
if(len(sys.argv)>1):
    user_url = sys.argv[1];
    if(len(sys.argv)>2):
        if(sys.argv[2]=="True"):
            isLocal=True;
        elif(sys.argv[2]=="False"):
            isLocal=False;
        else:
            print("Invalid input. Correct input format is:")
            cmnd_str = "python url_to_text.py"
            cmnd_args = "<url/absolute_path to file> <True/False>"
            print(cmnd_str)
            print("or")
            print(cmnd_str+cmnd_args)
            sys.exit();
    else:
        print("Invalid input. Correct input format is:")
        cmnd_str = "python url_to_text.py"
        cmnd_args = "<url/absolute_path to file> <True/False>"
        print(cmnd_str)
        print("or")
        print(cmnd_str+cmnd_args)
        sys.exit();

url_to_file = ""
local_file_path = ""
filetype= ""
ext=""

if(isLocal):
    if(not os.path.exists(user_url)):
        print("File path does not exist, please provide right file path.")
        sys.exit();

if(not isLocal):
    url_to_file = user_url;

    r = requests.get(url_to_file)
    content_type = r.headers.get('content-type')

    if 'application/pdf' in content_type:
        ext = '.pdf'
    elif 'text/html' in content_type:
        ext = '.html'
    elif 'text/plain' in content_type:
        ext = '.txt'
    else:
        ext = ''
        print('Unknown type: {}'.format(content_type))
        print('Please input only HTML/PDF/TXT files')
        sys.exit();

    print("Remote file, type = ",ext)
    filetype=ext;
else:
    local_file_path = user_url;

    #filetype = mimetypes.guess_extension(local_file_path)
    filetype = magic.from_file(local_file_path, mime = True)
    #filetype = pathlib.Path(local_file_path).suffix

    if 'application/pdf' in filetype:
        ext = '.pdf'
    elif 'text/html' in filetype:
        ext = '.html'
    elif 'text/plain' in filetype:
        ext = '.txt'
    else:
        ext = ''
        print('Unknown type')
        print('Please input only HTML/PDF/TXT files')
        sys.exit();
    print("Local file, type = ",ext)
    filetype=ext;



############################# HTML/PDF/TXT PROCESSING #################################3
abs_outfile_path = os.path.abspath("../output_files/outfile_inter.txt");
text_content_infile = open(abs_outfile_path,"w");

if(ext == ".html" ):

    # ------- Extracting text from a HTML URL ------------    
    html = "";

    if(not isLocal):
        url = user_url;
        html = urlopen(user_url).read()

    if(isLocal):
        HTMLFile = open(user_url, "r")
        # Reading the file
        html = HTMLFile.read()

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

    text_content_infile.write(text2);
    text_content_infile.close();


elif(ext == ".pdf" ):
    if(not isLocal):

        url = user_url;
        r = requests.get(url)
        f = io.BytesIO(r.content)
        text = extract_text(f)

        text_content_infile.write(text);
        text_content_infile.close();


    else:
        text = extract_text(local_file_path)
        text_content_infile.write(text);
        text_content_infile.close();

else:
    if(not isLocal):
        # ------- Extracting text from a HTML URL ------------    
        url = user_url;
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

        text_content_infile.write(text2);
        text_content_infile.close();

    else:
        txtfile = open(user_url,"r")
        lines = txtfile.readlines();
        for line in lines:
            text_content_infile.write(line[:-1]);
            text_content_infile.write("\n");
        text_content_infile.close();


#raw text content from PDF/HTML/TXT document now present in outfile_inter.txt

"""
Generic helper function that returns start and end index of the window of a given size 
containing the acronym
"""
def search(target, text, context):
    # It's easier to use re.findall to split the string, 
    # as we get rid of the punctuation
    words = re.findall(r'\w+', text)

    matches = (i for (i,w) in enumerate(words) if w == target)
    for index in matches:
        if index < context //2:
            yield words[0:context+1]
        elif index > len(words) - context//2 - 1:
            yield words[-(context+1):]
        else:
            yield words[index - context//2:index + context//2 + 1]


def build_window(acronym, text_file):
    
    size = len(acronym)*4;
    
    '''
    window_left_start_idx = max(acronym_start_idx - size, 0)
    window_left_end_idx = max(acronym_start_idx - 1, 0);
    window_right_start_idx = min(acronym_end_idx + size, lastchar_idx)
    window_right_end_idx = min(acronym_end_idx + 1, lastchar_idx)
    '''

    ### Core logic
    
    lst_words = list(search(acronym,text_file,size));

    return lst_words


"""
Function to get the expansion of the acronym
"""
def expansion_finder(text_windows, acronym):
    expansions = []
    

    ### Core logic
    for window in text_windows:
        idx = window.index(acronym)
        window[idx] = "*"
        #print(window)
        first_letters=[]
        for word in window:
            #print(word[0], type(word[0]))
            #fisrt_letters = str(first_letters +""+ str(word[0:1]))
            first_letters.append(word[0])
        first_letters = ''.join(first_letters)
        #print(first_letters)
        #found_indices = re.search(acronym, first_letters, re.IGNORECASE).start()
        found_indices = [_.start() for _ in re.finditer(acronym, first_letters,re.IGNORECASE)] 
        for idx in found_indices:
            exp_str = (' '.join(window[idx:idx+len(acronym)])).lower()
            if(exp_str not in expansions):
                expansions.append(exp_str)
        

    return expansions


fpath =  abs_outfile_path
text_file = ''
expansion_database = {}

with open(fpath,'r') as f:
    text_file = f.readlines()
    text_file = ' '.join(text_file)

acronym_list = set([x.group() for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text_file)])
print(acronym_list, len(acronym_list))

with open(fpath,'r') as f:
    text_file = re.sub(r"[^A-Za-z\.&]", " ", text_file)
    text_file = re.sub(r"\s+", " ", text_file)


for acronym in acronym_list:
    ## Routine to build a window from acronym_startidx, acronym_endidx, part of text of 100 chars around it
    #a=x.group() 
    acronym = re.sub(r"[^A-Za-z\.&]", "",acronym)
    text_windows = build_window(acronym, text_file);
    str_s = "%%% "+acronym+" %%%"
    print(str_s)
    #print(text_windows)
    print("============")
    
    ## Search for expansion
    lst_expansion = expansion_finder(text_windows, acronym)
    print(lst_expansion)

    ## Add to dictionary
    
