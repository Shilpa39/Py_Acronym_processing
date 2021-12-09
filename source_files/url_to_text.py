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



#user-defined variables - could be overridden by command line arguments
#user_url="https://raw.githubusercontent.com/mathmanu/caffe-jacinto-models/caffe-0.17/trained/image_classification/imagenet_jacintonet11v2/initial/test.prototxt"
#user_url="https://en.wikipedia.org/wiki/Baahubali_2:_The_Conclusion"
user_url="https://arxiv.org/pdf/1611.01228"
isLocal=False;

#user_url="/home/a0492783/Downloads/TI_C7X_DSP_TRAINING_00.06/c7x_dsp_isa/C7x_ISA_Database.html"
#user_url="/home/a0492783/Py_Acronym_processing/testcases/testcases_rawfiles/testcase1.pdf"
#user_url="/home/a0492783/Py_Acronym_processing/testcases/testcases_urls.txt"
#isLocal=True;

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
            cmnd_str = "python determine_filetype.py"
            cmnd_args = " <url_to_file> <True/False>"
            print(cmnd_str)
            print("or")
            print(cmnd_str+cmnd_args)
            sys.exit();
    else:
        print("Invalid input. Correct input format is:")
        cmnd_str = "python determine_filetype.py"
        cmnd_args = " <url_to_file> <True/False>"
        print(cmnd_str)
        print("or")
        print(cmnd_str+cmnd_args)
        sys.exit();

url_to_file = ""
local_file_path = ""
filetype= ""
ext=""

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
text_content_infile = open("../output_files/outfile_inter.txt","w");

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