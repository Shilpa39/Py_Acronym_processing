# importing the module

import requests
import magic
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup
import io
import urllib.request
from pdfminer.high_level import extract_text
import os
import re
import pandas as pd
import csv


def readAndProcessFile(isLocal, user_url, abs_outfile_path):
    local_file_path = ""

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
    else:
        local_file_path = user_url;
        filetype = magic.from_file(local_file_path, mime = True)

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
            sys.exit()
        print("Local file, type = ",ext)
        
    filetype=ext    
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

    return;

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


"""
Helper function that returns a window containing the acronym in list format
"""
def build_window(acronym, text_file, size):
    
    lst_words = list(search(acronym,text_file,size));

    return lst_words

"""
Function to get the expansion of the acronym
"""
def expansion_finder(text_file, acronym, max_window_size):
    expansions = []
    window_size = len(acronym)*4

    while (len(expansions) == 0 and window_size <= max_window_size):
        text_windows = build_window(acronym, text_file, window_size)

        for window in text_windows:
            idx = window.index(acronym)
            window[idx] = "*"
            #print(window)
            first_letters=[]
            for word in window:
                if(len(word)>1):
                    first_letters.append(word[0])
                else:
                    first_letters.append("*")
            first_letters = ''.join(first_letters)
            found_indices = [_.start() for _ in re.finditer(acronym, first_letters,re.IGNORECASE)] 
            for idx in found_indices:
                exp_str = (' '.join(window[idx:idx+len(acronym)])).lower()
                if(exp_str not in expansions):
                    expansions.append(exp_str)
        
        window_size *= 2
        
    return expansions

"""
Function that builds the acronym expansion database for a given document
"""
def buildAcronymDatabase(acronym_list, df, text_file, outPath = ''):
    for acronym in acronym_list:
        cleaned_acronym = re.sub(r"[^A-Za-z]", "",acronym)
        str_s = "%%% "+acronym+" %%%"
        print(str_s)
        print("============")
        
        ## Search for expansion
        lst_expansion = expansion_finder(text_file, cleaned_acronym, len(cleaned_acronym)*64)
        print(lst_expansion)
        
        if acronym not in df.Acronym.values:
            to_be_written = ';'.join(lst_expansion)
            df2 = pd.DataFrame([[acronym,to_be_written]], columns=['Acronym','Expansions'], index=[len(df)])
            df = df.append(df2, ignore_index=True)
            
        else:
            raw_expansions = df[df['Acronym']==acronym]['Expansions'].values
            database_expansions_list = []
            if((type(raw_expansions[0])==str)):
                database_expansions_list = raw_expansions[0].split(";")
            idx_acronym = df.index[df['Acronym']==acronym].tolist()[0];
            to_be_written = ';'.join(list(set().union(database_expansions_list, lst_expansion)));
            df.at[idx_acronym, "Expansions"] = to_be_written

    df.to_csv(outPath,index=False)
    print(df)

def main():
    # Process command line arguments
    if(len(sys.argv)>1):
        user_url = sys.argv[1]
        if(len(sys.argv)>2):
            if(sys.argv[2]=="True"):
                isLocal=True
            elif(sys.argv[2]=="False"):
                isLocal=False
            else:
                print("Invalid input. Correct input format is:")
                cmnd_str = "python pycronym.py"
                cmnd_args = " <url/absolute_path to file> <True/False>"
                print(cmnd_str)
                print("or")
                print(cmnd_str+cmnd_args)
                sys.exit()
        else:
            print("Invalid input. Correct input format is:")
            cmnd_str = "python pycronym.py"
            cmnd_args = " <url/absolute_path to file> <True/False>"
            print(cmnd_str)
            print("or")
            print(cmnd_str+cmnd_args)
            sys.exit()

    else:
        user_url="https://arxiv.org/pdf/2110.11694"
        isLocal=False;     
    
    abs_outfile_path = os.path.abspath("../output_files/outfile_inter.txt")
    readAndProcessFile(isLocal, user_url, abs_outfile_path)   

    text_file = ''
    with open(abs_outfile_path,'r') as f:
        text_file = f.readlines()
        text_file = ' '.join(text_file)

    # Clean Document
    text_file = re.sub(r"[^A-Za-z\.&]", " ", text_file)
    text_file = re.sub(r"\s+", " ", text_file)

    # Build list of unique acronyms from a document
    acronym_list = set([x.group() for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text_file)])

    # Remove pre existing database (old documents might cause issue)
    csv_outpath = "../output_files/database.csv"

    df = pd.read_csv(os.path.abspath(csv_outpath), usecols= ['Acronym','Expansions'])
    buildAcronymDatabase(acronym_list, df, text_file, csv_outpath)

if __name__ == "__main__":
    main()