from ebooklib import epub
from BeautifulSoup import BeautifulSoup
import nltk
import re
import matplotlib.pyplot as plt
import numpy as np
import csv

#------------- IRENE: SHIELD YOUR EYES ------------------
RE_PART_SPLIT = re.compile(r'OEBPS/part(\d+)_split_(\d+).xhtml')
RE_PART = re.compile(r'OEBPS/part(\d+).xhtml')

def get_sort_key(html_file):
    """Given a filename in the form of OEBPS/partXXX_split_XXX.xhtml, extract
       the part number and split number and return as a numeric tuple."""
    file_name = html_file.file_name
    match = RE_PART_SPLIT.search(file_name)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    
    match = RE_PART.search(file_name)
    if match:
        return (int(match.group(1)), 0)
    
    print('Warning, failed to match: ' + file_name)
    return None

def is_matching(html_file):
    """Given a filename, return true if it matches the OEBPS/partXXX.xhtml or
       OEBPS/partXXX_split_XXX.xhtml patterns."""
    return get_sort_key(html_file) is not None

def sort_html_files(html_files):
    """Given a list of epub.EpubHtml objects, return a copy of that list where
       the files are sorted by filename."""
    filtered_files = filter(is_matching, html_files)
    return sorted(filtered_files, key=get_sort_key)
#------------- IRENE: OK, YOU CAN LOOK NOW ---------------


def is_html(epub_file):
    """Given an file from an epub book object, returns true if it is an html 
       file."""
    return type(epub_file) is epub.EpubHtml

def get_html_files(epub_book):
    """Given a book from epub.read_epub, strip from the list of files everything
       that isn't an html."""
    result_list = []
    for epub_file in epub_book.items:
        if is_html(epub_file):
            result_list.append(epub_file)
    return result_list
    
# x.content is full file contents
# x.get_body_content() returns the contents of the <body> tag

def combine_html_files(html_files): 
    combined_text=''
    for index in range(len(html_files)):
        parsed_html = BeautifulSoup(html_files[index].content)
        html_text = parsed_html.getText('\n')
        combined_text = combined_text + html_text
    return combined_text

def names_list(csv_file):
    """ Given a csv file of characters, organizes a list of names"""
    charfile  = open(csv_file, "rb")
    reader = csv.reader(charfile)
    firstnames=[]
    names=[]
    for row in reader:
        if not row:
            continue
        firstnames.append(row[0])
        names.append(row)
        for i in range(len(firstnames)):
            firstnames[i] = firstnames[i].strip()
            for j in range(len(names[i])):
                names[i][j] = names[i][j].strip()
    charfile.close() 
    return [names, firstnames]
    
def track_person(list_of_tokens,persons):
    """Given a list of tokens, returns index for the character of interest"""
    person_indices=[] #this list is if you want the index for each occurrence
    occurrence = [0]*len(persons)    
    for row in range(len(persons)):
        for i in range(len(persons[row])):
            for j in range(len(list_of_tokens)):
                if list_of_tokens[j] == persons[row][i]:
                    person_indices.append(j)
                    occurrence[row] = occurrence[row] + 1
    return [person_indices, occurrence]  

book = epub.read_epub('01.epub')
html_files = get_html_files(book)
html_files = sort_html_files(html_files)    
booktext = combine_html_files(html_files)
tokens = nltk.word_tokenize(booktext)

chars_list = names_list('chars_test.csv')[0]
print chars_list
x_label = names_list('chars_test.csv')[1]
character_count = track_person(tokens, chars_list)[1]
print character_count
plt.bar(range(1,len(chars_list)+1), character_count, width=1)   
ax1=plt.gca()
ax1.set_xticks(range(1,len(x_label)+1))
ax1.set_xticklabels(x_label)
  
# x = track_person(tokens, 'Harry')[0]
# y = [1 for i in range(len(x))]
# plt.scatter(x,y)
plt.show()



