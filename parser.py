from ebooklib import epub
from BeautifulSoup import BeautifulSoup
import re
import os

def get_html_files_in_reading_order(book):
  """Given a book object created from `epub.read_epub(filename)`, return a
     list of html file objects, selected out of the epub manifest, and in
     the reading order specified by the spine."""
  html_files = list()

  # create a dictionary to hold the `idref` to `epubFile` mapping.
  idref_to_epub_file = dict()
  for item in book.items:
    idref_to_epub_file[item.id] = item

  for idref, linear in book.spine:
    if linear:
      epub_file = idref_to_epub_file.get(idref, None)
      assert epub_file, ("Broken spine for '{}', missing idref '{}'"
                         .format(book.title, idref))
      if isinstance(epub_file, epub.EpubHtml):
        html_files.append(epub_file)
  return html_files

kNewYorkTimesRegex = re.compile(r'[Nn]ew\s+[Yy]ork\s+[Tt]imes')
kAmazonComRegex = re.compile(r'[Aa]mazon\.[Cc]om')
kChapterRegex = re.compile(r'[Cc]hapter')
kCopyrightRegex = re.compile(r'[Cc]opyright')
kRightsReservedRegex = re.compile(r'[Aa]ll\s+[Rr]ights\s+[Rr]eserved');

def get_text_from_html_files(html_files):
  """Given a list of epub.HtmlFile objects, parse them with beautiful soup and
     return a corresponding list of text strings."""

  text_list = list()
  for html_file in html_files:
    parsed_html = BeautifulSoup(html_file.content)
    paragraphs = [x.getText() for x in parsed_html.find('body').findAll('p')]
    
    # This is probably front or back matter
    if len(paragraphs) < 10:
      continue

    file_text = '\n\n'.join(paragraphs)

    # The page is empty, probably a title page or something
    if len(file_text.strip()) == 0:
      continue

    # If the page has less than 1000 characters, then it is probably not a 
    # chapter
    if len(''.join(paragraphs)) < 1000:
      continue

    # If the word 'chapter' shows up more than 10 times, this is probably a
    # table of contents
    if len(kChapterRegex.findall(file_text)) > 10:
      continue

    # If either of these words show up in the text, it's probably an "acclaims"
    # page
    if (kNewYorkTimesRegex.search(file_text) 
        or kAmazonComRegex.search(file_text)):
      continue

    # This is almost certainly a copyright page
    if (kCopyrightRegex.search(file_text) 
        and kRightsReservedRegex.search(file_text)):
      continue

    text_list.append(file_text)
  return text_list



def parse_book(filename):
  """Combines above two functions into a single call."""
  book = epub.read_epub(filename)
  html_files = get_html_files_in_reading_order(book)
  return get_text_from_html_files(html_files)


kChapterTests = dict(
  #beyonders=[1+25, 2+28, 2+36],
  brotherband=[44], 
  #divergent= [39, 47+1],
  #harry_potter= [17, 18, 22, 37, 38, 30, 37],
)

def run_tests():
  this_dir = os.path.dirname(os.path.realpath(__file__))
  book_dir = os.path.join(this_dir, 'books')

  for series, num_chapter_list in kChapterTests.iteritems():
    for idx in range(len(num_chapter_list)):
      filename = '{}_{:02d}.epub'.format(series, idx+1)
      filepath = os.path.join(book_dir, filename)
      text_list = parse_book(filepath)
      n_chapters_actual = len(text_list)
      n_chapters_expected = num_chapter_list[idx]
      assert n_chapters_actual == n_chapters_expected, (
        "Expected {} chapters for {} but got {}\n"
        .format(n_chapters_expected, filename, n_chapters_actual))
      print "{}: OK".format(filename)

