# Using Data to Answer "What Makes a Good Story?" #

##Background##
How often do you hear someone asking "Have you read any good books lately?" Usually, the person asking this question has probably wasted hours of their life reading crappy books. When you login to amazon.com, you're given suggestions for what books you would like, based on the books you've already read. Unfortunately, their algorithm for finding interesting books seems to be limited to -*I see you've read the Hunger Games ... here are some more Dystopian novels for you. Maybe you should try the Twilight series - it's also popular, young adult fiction.* Meh - not helpful. Personally, I like all sorts of books. I've read over 100 classic novels, and am a fan of Dohtstoyevsky, but I also enjoy reading Harry Potter and similar young adult fantasy. Just because I've enjoyed a couple books from a particular genre, doesn't mean that I only want to read books from that genre! So I find myself wondering whether good stories are completely independent of genre. Perhaps good stories succeed in striking a pleasant balance between character depth and character breadth, in addition to having a reasonable plot. The catch here is that some people don't care about character breadth (think about The Metamorphosis by Franz Kafka, where the entire story is a window into the mind of a single character), and some people prefer books with enormous breadth (honestly, I couldn't keep track of the characters in One Hundred Years of Solitude). If you could search for books based on character depth versus breadth or style of storytelling, would you avoid wasting time reading crappy books?

##Hypothesis##
Quantifying patterns in stories, including character breadth versus character depth, can help you identify the types of books that you enjoy reading. In this way, data can help us answer the question of "what makes a good story?" (which is of course, dependent on the user's personal reading preferences but not necessarily dependent on genre). 

## Methodology ##
I used Python to extract data from several electronic books (epubs) within the broad category of "young adult fiction." To start, I chose to focus on character patterns.

### Initial Approach ###
I started analysing the Harry Potter series first. This choice was driven by the online availability of a full character list for these books. I began by using the Natural Language Toolkit (NLTK) library to convert epubs into lists of strings (i.e., tokens). In this way, I was able to search for tokens like "Harry" or "Ron" and then count the number of times these characters were mentioned throughout the book. Below is a snapshot of some of this data. It's very obvious that Harry is mentioned quite a number of times throughout book 1. At this point, the data isn't really telling me anything that I didn't already know.

![hpbook1_names.png](https://bitbucket.org/repo/Mx7pKn/images/2946209153-hpbook1_names.png)

Next, I looked at how frequently characters were mentioned over an entire book, and what the distribution of "main" characters versus "minor" characters looked like. The plot below compares the first book in the Harry Potter series (top graph) to the last book in the series (bottom graph). As you can see, the series starts out with an obvious protagonist (Harry). He is mentioned over 1000 times in book 1. The top plot also shows that there are nearly 10 "minor" characters which are mentioned between 100-200x throughout the novel. By book 7, the number of characters mentioned in the book has grown by quite a lot. Harry is no longer the only character mentioned over 1000 times. In fact, there are a couple characters mentioned over 550 times, and nearly 25 "minor" characters who are mentioned only 100-150x. 

![hp1_7subplot.png](https://bitbucket.org/repo/Mx7pKn/images/2061119558-hp1_7subplot.png)

Compare how the Harry Potter series progresses to the Maze Runner series by James Dashner. As shown in the plot below, there is a main character that is mentioned over 1000 times throughout the novels. The number of main characters in this series actually shrinks as the series progresses. Unlike the Harry Potter series, where minor characters are increasingly developed into main characters, the Maze Runner series focuses on the protagonist alone and does not provide character depth to anyone else in the book. 

![mazerunner1_3subplots.png](https://bitbucket.org/repo/Mx7pKn/images/625874408-mazerunner1_3subplots.png)

Already, the data is starting to reveal how character breadth and depth varies for different books. Next, I wanted to explore this concept over the progression of a novel and over the progression of a series of novels.

### Final Approach ###
In order to better understand character depth and breadth in a given series of books, I refined my initial approach to examine the number of characters in each chapter throughout a series. I also refined the data by plotting separate bars based on the number of times each character was mentioned in the chapter. Specifically, the grey bars in the plots below show the total number of characters mentioned in each chapter (including very minor characters). The red bars filter out characters who were mentioned less than 3 times. Characters mentioned less than 3 times likely represent "noise" because they are probably not interacting with the main character. The blue bars represent dominant characters in the chapter, and filter out characters who were mentioned less than 15 times. 

Before I looked at the data from the remaining epubs, I made a list of the books which I planned to analyse. Then I ranked them in order of how much I liked that book. In order of most to least favorite:

* Harry Potter series by J.K. Rowling
* Brotherband chronicles by John Flanagan tied with the Beyonders series by Brandon Mull
* Hunger Games series by Suzanne Collins
* Maze Runner series by James Dashner
* Divergent series by Veronica Roth (I couldn't even bear finishing this series)

Notably, for each series, I tried to use the NLTK library to tag all proper pronouns in a given book, in an attempt to extract a list of all characters in the book (after all, I don't remember all the minor characters from books that I read 5 years ago). I found out that the library was unable to successfully tag all of the proper pronouns. I did not expect the code to be able to distinguish between places and names ("Hogwarts" and "Harry" are both proper pronouns). I was disappointed to find that the code was tagging random words like "Please" and "Unless" which are definitely not proper pronouns. I attempted to also filter out tagged words which occurred less than 4 times. This assumes that characters who are only mentioned 3 times are insignificant to the story (i.e., I do not even consider them to be minor characters). In the end, I had to do a lot of manual editing. I sorted the output by frequency of occurrence, and deleted words from the bottom of the list which were clearly not names. For all words that I was unsure of, I looked each up online to figure out if it was actually a character or not. For instance "Felrook" from the Beyonders series is a location, not a person (and I could not remember this).

Identifying the start of a new chapter was another challenge that required special attention. Some epubs contain a table of contents (toc), and the chapters are sorted based on toc. Other epubs are lacking a proper table of contents, but I am able to search for the token "Chapter" in order to identify the indices for all new chapters. That approach required some manual checking to make sure that "Chapter" was actually the start of a new section. Of course, there are probably epubs that have neither a toc nor sections labelled with "Chapter." That's something I'll have to troubleshoot later, if I continue to develop this project.

## Key Results ##
Below are the character patterns for each of the Harry Potter books, plotted according to chapter progression:
![hp1_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/1442896934-hp1_bychapter.png)
![hp2_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/2211721534-hp2_bychapter.png)
![hp3_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/3349945148-hp3_bychapter.png)
![hp4_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/2037694172-hp4_bychapter.png)
![hp5_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/2320447020-hp5_bychapter.png)
![hp6_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/3254033752-hp6_bychapter.png)
![hp7_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/3641079957-hp7_bychapter.png)

Note that the Harry Potter books are all plotted up to a y-axis value of 70. I noticed that no other book that I analyzed had so many characters. The remaining plots are all shown with a max y-axis value of 30. 

![brotherband1.png](https://bitbucket.org/repo/Mx7pKn/images/3728856753-brotherband1.png)
![brotherband2.png](https://bitbucket.org/repo/Mx7pKn/images/1715254307-brotherband2.png)
![brotherband3.png](https://bitbucket.org/repo/Mx7pKn/images/4144328460-brotherband3.png)

![beyonders1.png](https://bitbucket.org/repo/Mx7pKn/images/1102671954-beyonders1.png)
![beyonders2.png](https://bitbucket.org/repo/Mx7pKn/images/3087977819-beyonders2.png)
![beyonders3.png](https://bitbucket.org/repo/Mx7pKn/images/58032596-beyonders3.png)

![hungergames1.png](https://bitbucket.org/repo/Mx7pKn/images/3362662986-hungergames1.png)
![hungergames2.png](https://bitbucket.org/repo/Mx7pKn/images/205217570-hungergames2.png)
![hungergames3.png](https://bitbucket.org/repo/Mx7pKn/images/848505291-hungergames3.png)

![mazerunner1.png](https://bitbucket.org/repo/Mx7pKn/images/1411760702-mazerunner1.png)
![mazerunner2.png](https://bitbucket.org/repo/Mx7pKn/images/3450592742-mazerunner2.png)
![mazerunner3.png](https://bitbucket.org/repo/Mx7pKn/images/2984717330-mazerunner3.png)

![divergent1.png](https://bitbucket.org/repo/Mx7pKn/images/2224003594-divergent1.png)
![divergent2.png](https://bitbucket.org/repo/Mx7pKn/images/765769502-divergent2.png)
![divergent3.png](https://bitbucket.org/repo/Mx7pKn/images/2637047517-divergent3.png)

## Initial Conclusions ##
The preliminary results show that there are indeed some qualitative trends in the style of storytelling that I prefer. I like the Harry Potter books the most, and perhaps that means I enjoy novels with impressive character breadth. I interact with many people per day, and perhaps the large number of characters in the Harry Potter books agrees with how I feel people interact on a regular basis. The Harry Potter books are not without character depth, however. There are apparent "dips" in the data, which occur more and more frequently as the series progresses. I can hypothesize that these dips represent chapters in which the author chooses to provide additional depth to new characters. Understanding what these dips represent requires further analysis.

The plots for the Beyonders and Brotherband books look quite different. There isn't a lot of character "noise" in the Beyonders series, and the blue bars are relatively large compared to the grey bars. The Brotherband books have a more even distribution of blue, red, and grey. Interestingly, the Divergent series (my least favorite books) have the smallest blue bars. Given this observation, it's tempting to conclude that I like books which have more than 1 main character per chapter (i.e., the blue bars are consistently greater than 1). But there are a lot of assumptions that I made with this data (see below), and I don't think I currently have enough evidence to make any final conclusions. 

So far, even these superficial results have provided insight into the method of storytelling for different authors. This project, of course, is a work in progress. The results presented here were based on a few weeks of work. Hopefully, I can think of new ways to visualize the data and make more concrete conclusions in time.  

## Assumptions ##

* When creating the character lists, I deleted last names and prefaces such as "Professor" to avoid double counting. The assumption here is that characters are usually referred to by one name more than the other.  This also helps to avoid confusion over shared family names.
* There is some error in creating the list of characters in a series. I ignored characters that were only mentioned < 5 times. 
* There is a subtle assumption that chapter lengths are more or less similar across a particular book, and across different series. I describe this assumption as "subtle" only because I am *comparing* different series. For instance, the Maze Runner series has a lot more chapters than some of the other novels I analysed. If the chapters are shorter, perhaps this means the cut-off for the blue and red bars should be changed. Right now, I define "main characters" as those who are mentioned at least 15 times in the chapter. If the chapter is really short, perhaps this threshold needs to be 10x rather than 15x. 

## Future Work ##

* Add more books, including fiction outside the scope of "young adult."
* Create interactive plots to make the data easier to digest.
* Explore how to characterize the "dips" described above. Do these dips represent character development, or are these dips chapters full of action, epic battles, etc.
* Normalize the data according to chapter length. Perhaps this means that chapter length will automatically determine the thresholds for the red and blue bars.