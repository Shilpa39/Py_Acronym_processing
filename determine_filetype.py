import requests
import mimetypes
import magic
import pathlib
import sys

#user-defined variables - could be overridden by command line arguments
user_url="https://raw.githubusercontent.com/mathmanu/caffe-jacinto-models/caffe-0.17/trained/image_classification/imagenet_jacintonet11v2/initial/test.prototxt"
isLocal=False;

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

