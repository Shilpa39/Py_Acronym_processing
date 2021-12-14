# Py_Acronym_processing
This is the repository for document processing for detection and expansion of acronyms using Python3

# Required Packages
Ensure that the latest versions of python and pip are installed. It is recommended to use a separate evironment so that there is no interference with packages installed on your system. We recommend [Anaconda environment manager](https://www.anaconda.com/products/individual) package manager for this purpose. It is not a requirement to get an evironment manager.

To install all the required packages run the following command from terminal

```console
~/Py_Acronym_processing$ sudo apt-get install libmagic1
~/Py_Acronym_processing$ pip install python-magic requests pandas pdfminer.six beautifulsoup4
```

# How to Use
From the parent directory, navigate to the source_files
```console
~/Py_Acronym_processing$ cd source_files
~/Py_Acronym_processing/source_files$ python init_files.py
~/Py_Acronym_processing/source_files$ python pycronym.py <url/absolute_path to file1> <True/False>
~/Py_Acronym_processing/source_files$ python pycronym.py <url/absolute_path to file2> <True/False>
.
.
```

The first command line argument is either the URL or the absolute path (if file is located on host).The second command line argument is used to clear the database before single/multiple documents are passed to build the database of acronyms. The third command line argument indicates whether or not the file is hosted locally or not (True if it is a local path, False if not). Both arguments are mandatory.

If you want to see an example of the application running, simply run the command without arguments. It will get the acronyms from the following PDF document: https://arxiv.org/pdf/2110.11694

```console
~/Py_Acronym_processing/source_files$ python pycronym.py
```

# Further Improvements

<ol>
    <li> Recommender system to recommend most likely expansion based on a global database derived of various documents and context of the acronym. </li>
    <li> Link in database for scalability. Also need to consider cases where search span can be larger than available RAM and organize memory fetch accordingly. </li>
</ol>
