from ebooklib import epub
from BeautifulSoup import BeautifulSoup
import nltk
import re

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
    
book = epub.read_epub('01.epub')
html_files = get_html_files(book)
html_files = sort_html_files(html_files)

# x.content is full file contents
# x.get_body_content() returns the contents of the <body> tag

# html = #the HTML code you've written above

def combine_html_files(html_files): 
    combined_text=''
    for index in range(len(html_files)):
        parsed_html = BeautifulSoup(html_files[index].content)
        html_text = parsed_html.getText('\n')
        combined_text = combined_text + html_text
    return combined_text

def track_person(list_of_tokens,person):
    """Given a list of tokens, returns the index for the word Harry"""
    person_indices=[]
    for index in range(len(list_of_tokens)):
        if list_of_tokens[index] == person:
            person_indices.append(index)
    return person_indices
    
booktext = combine_html_files(html_files)
tokens = nltk.word_tokenize(booktext)


   
        

