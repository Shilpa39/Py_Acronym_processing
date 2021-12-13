import re
import os

abs_file_path = os.path.abspath("../output_files/outfile_inter.txt");
#abspath = os.getcwd()
#print(abspath)
#print(__file__)
text_file = open(abs_file_path,"r");
text_file = text_file.readlines();
text_file = ' '.join(text_file)

acronym_list = set([x.group() for x in re.finditer(r'\b[A-Z](?=([&.]?))(?:\1[A-Z]){1,5}\b', text_file)])

print(acronym_list)