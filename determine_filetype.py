import requests
import mimetypes
import magic
import pathlib

#user-defined variables
user_url="/home/a0492783/Py_Acronym_processing/myfile.pdf"
isLocal=True;


#code starts here
url_to_file = ""
local_file_path = ""
filetype= ""

if(not isLocal):
    url_to_file = user_url;

    r = requests.get(url_to_file)
    content_type = r.headers.get('content-type')
    ext=""

    if 'application/pdf' in content_type:
        ext = '.pdf'
    elif 'text/html' in content_type:
        ext = '.html'
    else:
        ext = ''
        print('Unknown type: {}'.format(content_type))

    print("Remote file, type = ",ext)
    filetype=ext;
else:
    local_file_path = user_url;

    #filetype = mimetypes.guess_extension(local_file_path)
    #filetype = magic.from_file(local_file_path, mime = True)
    filetype = pathlib.Path(local_file_path).suffix
    print("Local file, type = ",filetype)

