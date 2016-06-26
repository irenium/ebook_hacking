from ebooklib import epub
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as ET
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

def get_body_node(node):
  for child in node.getchildren():
    if child.tag == '{http://www.w3.org/1999/xhtml}body':
      return child
  return None

kInlineSet = set(['span', 'a', 'b', 'i', 'br', 'em', 'strong', 'samp'])
kDeleteSet = set(['svg', 'table', 'hr', 'img', 'h1', 'h2', 'h3', 'blockquote', 'pagebreak', 'state', 'placename', 'placetype'])

def get_short_tag(node):
  namespace_end = node.tag.find('}') + 1
  return node.tag[namespace_end:]

def rewrite_node(node):
  text = node.text or ''
  for child in node.getchildren():
    text += rewrite_node(child)
    text += child.tail or ''
  return text

def rewrite_paragraph(node):
  text = node.text or ''
  for child in node.getchildren():
    # TODO(josh): validate tag type, we should only accept any inline block
    # tags
    if get_short_tag(child) in kInlineSet:
      text += rewrite_node(child)
      text += child.tail or ''
    elif get_short_tag(child) in kDeleteSet:
      text += child.tail or ''
    else:
      raise ValueError('Invalid tag {}'.format(get_short_tag(child)))
  return text + '\n'

def rewrite_div(node):
  text = ''
  for child in node.getchildren():
    if get_short_tag(child) == 'div':
      text += rewrite_div(child)
      text += node.tail or ''
    elif get_short_tag(child) == 'p':
      text += rewrite_paragraph(child)
      text += child.tail or ''
    elif get_short_tag(child) in kInlineSet:
      text += rewrite_node(child)
      text += child.tail or ''
    elif get_short_tag(child) in kDeleteSet:
      text += child.tail or ''
    else:
      raise ValueError('Invalid tag {}'.format(get_short_tag(child)))
  return text + '\n'

def parse_html(html_content):
  root = ET.fromstring(html_content)
  body = get_body_node(root)

  text = ''
  for child in body.getchildren():
    if get_short_tag(child) == 'p':
      text += rewrite_paragraph(child)
      text += child.tail or ''
    elif get_short_tag(child) == 'div':
      text += rewrite_div(child)
      text += child.tail or ''
    elif get_short_tag(child) in kInlineSet:
      text += rewrite_node(child)
      text += child.tail or ''
    elif get_short_tag(child) in kDeleteSet:
      text += child.tail or ''
    else:
      raise ValueError('Invalid root tag {}'.format(get_short_tag(child)))
  return text

def get_text_from_html_files(html_files):
  """Given a list of epub.HtmlFile objects, parse them with beautiful soup and
     return a corresponding list of text strings."""

  text_list = list()
  for html_file in html_files:
    text = parse_html(html_file.content)

    # The page is empty, probably a title page or something
    if not text.strip():
      continue

    # If the page has less than 1000 characters, then it is probably not a 
    # chapter
    if len(text) < 1000:
      continue

    # If the word 'chapter' shows up more than 10 times, this is probably a
    # table of contents
    if len(kChapterRegex.findall(text)) > 10:
      continue

    # If either of these words show up in the text, it's probably an "acclaims"
    # page
    if (kNewYorkTimesRegex.search(text) 
        or kAmazonComRegex.search(text)):
      continue

    # This is almost certainly a copyright page
    if kCopyrightRegex.search(text):
      continue

    text_list.append(text)
  return text_list



def parse_book(filename):
  """Combines above two functions into a single call."""
  book = epub.read_epub(filename)
  html_files = get_html_files_in_reading_order(book)
  return get_text_from_html_files(html_files)


kChapterTests = dict(
  beyonders=[2+25, 3+28, 4+36],
  brotherband=[1+44, 2+42, 1+47, 1+56, ], #1+51], 
  divergent= [1+39, 1+47], # 1+56],
  fablehaven= [19, 21, 18-14, 15-11, 31+3, 39+2],
  harry_potter= [17, 18, 22, 37, 38, 30, 37],
  # hunger_games= [27, 27, 28],
  maze_runner=[1+62, ] #65, 73+1],
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


if __name__ == '__main__':
  run_tests()