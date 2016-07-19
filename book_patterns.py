from ebooklib import epub
from BeautifulSoup import BeautifulSoup
import nltk
from nltk.tag import pos_tag
import re
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
from parser import parse_book

#-------old stuff ----------------------------------------------------------
def is_matching(html_file):
    """Given a filename, return true if it matches the OEBPS/partXXX.xhtml or
       OEBPS/partXXX_split_XXX.xhtml patterns."""
    return get_sort_key(html_file) is not None
    
def do_chapter_analysis():
    epub_paths = ['{:02d}.epub'.format(i+1) for i in range(7)]
    for epub_path in epub_paths:
        print "\n\n"
        book = epub.read_epub(epub_path)
        html_files = get_html_files(book)
        html_files = sort_html_files(html_files)
        print "Book {} has {} html files".format(epub_path, len(html_files))
        for html_file in html_files:
            parsed_html = BeautifulSoup(html_file.content)
            html_text = parsed_html.getText('\n')
            tokens = nltk.word_tokenize(html_text)
            token_iter = iter(tokens)
            for token in token_iter:
                if token.lower().startswith('chap'):
                    print "{} {}".format(token, next(token_iter))
                    break
            print re.sub('\s+', ' ', html_text[0:1000])
           
    sys.exit(0) 
    
def mentions_per_chapter2(list_of_tokens, persons, title, threshold):
    """Plots the number of characters in each chapter, based on how frequently 
    the character is mentioned. No different than the previous function, except 
    this function takes in tokens rather than strings"""
    chapter_indices = get_chapterindex(list_of_tokens) 
    person_indices = [list() for i in range(len(persons))] 

    #start by getting the indices for the mentions over the entire book
    for row in range(len(persons)):
        for i in range(len(persons[row])):
            for j in range(len(list_of_tokens)):
                if list_of_tokens[j] == persons[row][i]:
                    person_indices[row].append(j)

    #next add up how many times a given character is mentioned in each chapter
    num_per_chapter = [[0]*len(chapter_indices) for i in range(len(persons))]      
    for row in range(len(person_indices)):
        for i in range(len(person_indices[row])): 
            for j in range(len(chapter_indices)):
                if (person_indices[row][i] < chapter_indices[j] 
                    and person_indices[row][i] >= chapter_indices[j-1]):
                    num_per_chapter[row][j-1] = num_per_chapter[row][j-1]+1
            if person_indices[row][i] >= max(chapter_indices):
                num_per_chapter[row][-1] = num_per_chapter[row][-1]+1        
    
    #plot the # of characters per chapter
    x_label = range(1,len(chapter_indices)+1,1) #chapters in book
    char_per_chapter = [0]*len(x_label)
    main_chars = [0]*len(x_label)
    main_chars2 = [0]*len(x_label)
    for row in range(len(num_per_chapter)):
        for i in range(len(num_per_chapter[row])):
            if num_per_chapter[row][i] == 0:
                continue
            if num_per_chapter[row][i] != 0:
                char_per_chapter[i] = char_per_chapter[i]+1
            if num_per_chapter[row][i] > 2:
                main_chars[i] = main_chars[i]+1
            if num_per_chapter[row][i] > 14:
                main_chars2[i] = main_chars2[i]+1
                                                        
    p1 = plt.bar(range(1,len(char_per_chapter)+1), char_per_chapter, width=1)  
    p2 = plt.bar(range(1,len(char_per_chapter)+1), main_chars, width=1, 
    color='r')    
    p3 = plt.bar(range(1,len(char_per_chapter)+1), main_chars2, width=1, 
    color='y')
    ax1=plt.gca()
    ax1.set_xticks(range(1,len(x_label)+1))
    ax1.set_xticklabels(x_label)
    plt.title(title, fontsize=20)
    plt.xlabel('Chapter Number', fontsize=18)
    plt.ylabel('Number of Characters per Chapter', fontsize=18)
    plt.show()
    return       
#--------end old stuff-----------------------------------------------------

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

def sort_html_files(html_files, toc):
    """Given a list of epub.EpubHtml objects, return a copy of that list where
       the files are sorted by filename."""
    sorted_files=[]
    for i in range(len(toc)):
        for j in range(len(html_files)):
            if toc[i].href == html_files[j].file_name:
                sorted_files.append(html_files[j])
    return sorted_files

def combine_html_files(html_files): 
    combined_text=''
    for index in range(len(html_files)):
        parsed_html = BeautifulSoup(html_files[index].content)
        html_text = parsed_html.getText('\n')
        combined_text = combined_text + html_text
    return combined_text
    
def tokenize2(epub_input):
    """Uses the Natural Language Toolkit (nltk) to convert epubs into a list of
    strings (i.e., tokens)"""
    book = epub.read_epub(epub_input)
    html_files = get_html_files(book)
    toc = book.toc
    html_files = sort_html_files(html_files, toc)   
    booktext = combine_html_files(html_files)
    return nltk.word_tokenize(booktext)
        
def tokenize(epub_filename):
    """Uses the Natural Language Toolkit (nltk) to convert epubs into a list of
    strings (i.e., tokens)"""
    chapters = parse_book(epub_filename)
    booktext = '\n'.join(chapters)
    return nltk.word_tokenize(booktext)

def get_chapterindex(tokens):
    """Outputs the index numbers for the start of each new chapter"""
    chapter_indices = []
    for i in range(len(tokens)):
        if tokens[i] == 'CHAPTER':
            chapter_indices.append(i)
    return chapter_indices    
    
def propernouns(tokens):
    """Uses nltk to identify tokens which have been tagged as proper nouns"""
    tagged_sent = pos_tag(tokens)
    allpropernouns = [word for word,pos in tagged_sent if pos == 'NNP']
    
    # Stores a map of each proper noun to # of occurences of that proper noun
    noun_count = dict()
    for word in allpropernouns:
        if word in noun_count:
            noun_count[word] += 1
        else:
            noun_count[word] = 1
   
    propernouns = []
    noun_pairs = []
    for word, count in noun_count.iteritems():
        noun_pairs.append((count, word))
        #Proper nouns occurring <4x are probably not characters worth tracking
        if count > 3:  
            propernouns.append(word)    
    
    #Print out the list of proper nouns and the # times it's mentioned        
    noun_pairs = sorted(noun_pairs, reverse=True)
    for count, word in noun_pairs:
        print u'{:10s} {}'.format(word, count)
    print 'There are {} proper nouns'.format(len(propernouns))
    return propernouns

def names_list(csv_file):
    """ Given a csv file of characters, organizes a list of names"""
    charfile  = open(csv_file, "rb")
    reader = csv.reader(charfile)
    firstnames=[] #I use first names only for an x-axis label
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
    
def plot_names(persons, count, title):
    """Plots the number of times each character is mentioned (# vs name)"""
    x_label = names_list('hpchars.csv')[1]    
    plt.bar(range(1,len(persons)+1), count, width=1)   
    ax1=plt.gca()
    ax1.set_xticks(range(1,len(x_label)+1))
    ax1.set_xticklabels(x_label, rotation=90)
    plt.title(title, fontsize=20)
    plt.ylabel('Number of Mentions', fontsize=18)
    plt.show()
    return 
    
def track_person(list_of_tokens, persons):
    """Given a list of tokens, returns # of times each character is mentioned 
    over the entire book (i.e., character occurrence)""" 
    person_indices=[] #use this if you want the indices for character of interest   
    occurrence = [0]*len(persons) 
    for row in range(len(persons)):
        for i in range(len(persons[row])):
            for j in range(len(list_of_tokens)):
                if list_of_tokens[j] == persons[row][i]:
                    occurrence[row] = occurrence[row] + 1
                    person_indices.append(j)
    return [occurrence, person_indices]  

def mentions_per_chapter(chapter_strings, chars_csv, title, threshold):
    """Plots the number of characters in each chapter, based on how frequently 
    the character is mentioned"""
    chaptokens = []
    persons = names_list(chars_csv)[0]
    for chap in chapter_strings:
        chaptokens.append(nltk.word_tokenize(chap))
    
    #Count # of times each person is mentioned per chapter from the list persons    
    num_per_chapter = [[0]*len(chaptokens) for i in range(len(persons))]          
    for char in range(len(persons)):
        for name in range(len(persons[char])):
            for chap in range(len(chaptokens)):
                for i in range(len(chaptokens[chap])):
                    if chaptokens[chap][i] == persons[char][name]:
                        num_per_chapter[char][chap] += 1

    #Plot the # of characters per chapter
    x_label = range(1,len(chaptokens)+1,1) #chapters in book
    char_per_chapter = [0]*len(x_label)
    main_chars = [0]*len(x_label)
    main_chars2 = [0]*len(x_label)
    for row in range(len(num_per_chapter)):
        for i in range(len(num_per_chapter[row])):
            if num_per_chapter[row][i] == 0:
                continue
            if num_per_chapter[row][i] != 0:
                char_per_chapter[i] = char_per_chapter[i]+1
            #Characters which occur less than 3x are very minor characters
            if num_per_chapter[row][i] > 2:
                main_chars[i] = main_chars[i]+1
            #Characters which occur more frequently are the main characters 
            if num_per_chapter[row][i] > threshold: 
                main_chars2[i] = main_chars2[i]+1
    if threshold == 'none':
        p1 = plt.bar(range(1,len(char_per_chapter)+1), char_per_chapter, width=1, 
        alpha=0.75, color='0.75',edgecolor='w')  
    elif threshold == 3:
        p1 = plt.bar(range(1,len(char_per_chapter)+1), char_per_chapter, width=1, 
        alpha=0.75, color='0.75',edgecolor='w') 
        p2 = plt.bar(range(1,len(char_per_chapter)+1), main_chars, width=1,alpha=0.5,
        color='r',edgecolor='w')
    else:
        p1 = plt.bar(range(1,len(char_per_chapter)+1), char_per_chapter, width=1, 
        alpha=0.75, color='0.75',edgecolor='w') 
        p2 = plt.bar(range(1,len(char_per_chapter)+1), main_chars, width=1,alpha=0.5,
        color='r',edgecolor='w')    
        p3 = plt.bar(range(1,len(char_per_chapter)+1), main_chars2, width=1,
        alpha=0.8, color='#66b3ff',edgecolor='w')
    ax1=plt.gca()
    ax1.set_xticks(range(1,len(x_label)+1))
    ax1.set_xticklabels(x_label)
    plt.title(title, fontsize=20)
    plt.xlabel('Chapter Number', fontsize=18)
    plt.ylabel('Number of Characters per Chapter', fontsize=18)
    plt.ylim([0,70])
    plt.show()
    return                        

def count_mentions(persons, count):
    """Given a list of characters, and the number of times each character is
    mentioned in the book, counts the # of characters vs # of mentions"""
    #program should ignore zeros (characters do not appear in book at all)
    x_label = range(50,1050,50)
    y_count = [0]*len(x_label)

    for i in range(len(count)):
        if count[i] == 0:
            continue
        if count[i] > 1050:
            y_count[-1] = y_count[-1]+1  
        for j in range(len(x_label)):                
            if count[i] <= x_label[j] and count[i] > x_label[j-1]:
                y_count[j] = y_count[j]+1           
    return [x_label, y_count]

def subplot_count(file_list, csv_charfile, title):
    """Given a list of epubs, returns the # of mentions for each book"""
    x_label = range(50,1050,50)  
    tokens = [0]*len(file_list)
    character_count = [0]*len(file_list)
    y = [0]*len(file_list)
    chars_list = names_list(csv_charfile)[0]
    num_of_plots = len(file_list)
    f, ax = plt.subplots(num_of_plots, sharex=True, sharey=True)
    if num_of_plots == 1:
        ax = [ax]
    for i in range(len(file_list)):
        tokens[i] = tokenize(file_list[i])
        character_count[i] = track_person(tokens[i], chars_list)[0]
        y[i]= count_mentions(chars_list, character_count[i])[1]        
        ax[i].bar(range(1,len(x_label)+1), y[i], width=1, alpha=0.5,
        color='r',edgecolor='w')
   
    ax[0].set_title(title,fontsize=18)    
    ax[0].set_xticks(range(1,len(x_label)+1))
    ax[0].set_xticklabels(x_label)
    plt.xlabel('Number of Mentions Per Book', fontsize=18)
    plt.ylabel('                            Number of Characters', fontsize=18)
    plt.show()  
    return y
       
#chapter_strings = parse_book('brotherband3.epub')
#tokens = tokenize2('01hp.epub')  
#propernouns(tokens)
#chars_list = names_list('brotherband_chars.csv')[0]
#mentions_per_chapter(chapter_strings, 'brotherband_chars.csv', 'Brotherband','none')
#get_chapterindex(tokens)  
#subplot_count(['mazerunner1.epub','mazerunner2.epub'],'mazerunner_chars.csv',
#'Number of Maze Runner Characters in Books 1 & 3')
#character_count = track_person(tokens, chars_list)[0]
#plot_names(chars_list, character_count)

#x = track_person(tokens, 'Harry')[1]
#print x
#y = [1 for i in range(len(x))]
#plt.scatter(x,y)
