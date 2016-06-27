# Using Data to Answer "What Makes a Good Story?" #

##Background##
How often do you hear someone asking "Have you read any good books lately?" Usually, the person asking this question has probably wasted hours of their life reading crappy books. When you login to amazon.com, you're given suggestions for what books you would like, based on the books you've already read. Unfortunately, their algorithm for finding interesting books seems to be limited to *I see you've read the Hunger Games ... here are some more Dystopian novels for you. Maybe you should try the Twilight series - it's also popular, young adult fiction.* Meh - not helpful. In reality, I like all sorts of books. I've read over 100 classic novels, and am a fan of Dostoyevsky, but I also enjoy reading Harry Potter and similar young adult fantasy. And just because I've enjoyed a couple books from a particular genre, doesn't mean I only want to read books from that genre! I would guess that a good story is independent of genre, and strikes a certain balance between character depth and character breadth. The catch here is that some people don't care about character breadth (think about The Metamorphosis by Franz Kafka, where the entire story is a window into the mind of a single character), and some people prefer books with enormous breadth (honestly, I couldn't keep track of the characters in One Hundred Years of Solitude).

##Hypothesis##
Quantifying patterns in stories, including character breadth versus character depth, can help you identify the types of books that you enjoy reading. In this way, data can help us answer the question of "what makes a good story?" (which is of course, dependent on the user's personal reading preferences but not necessarily dependent on genre). 

## Methodology ##

I used Python to extract data from several electronic books (epubs) within the broad category of "young adult fiction." I chose to focus on character patterns throughout a story, and refined my approach as I explored the data.

### Initial Approach ###
I started analyzing the Harry Potter series first. This choice was driven by the online availability of a full character list for these books. I began by using the Natural Language Toolkit (NLTK) library to convert epubs into lists of strings (i.e., tokens). In this way, you are able to search for tokens like "Harry" or "Ron" and then count the number of times these characters are mentioned throughout the novel. Below is a snapshot of some of this data. It's very obvious that Harry is mentioned quite a number of times throughout book 1. At this point, the data isn't really telling me anything that I didn't already know.

![hpbook1_names.png](https://bitbucket.org/repo/Mx7pKn/images/2946209153-hpbook1_names.png)

Next, I looked at how frequently characters were mentioned over an entire book, and what the distribution of "main" characters vs "minor" characters was. The plot below compares the first book in the Harry Potter series (top graph) to the last book in the series (bottom graph). As you can see, the series starts out with an obvious protagonist (Harry). He is mentioned over 1000 times in book 1. The top plot also shows that there are nearly 10 "minor" characters which are mentioned between 100-200x throughout the novel. By book 7, the number of characters mentioned in the book has grown by quite a lot. Harry is no longer the only character mentioned over 1000 times. In fact, there are a couple characters mentioned over 550 times, and nearly 25 "minor" characters who are mentioned only 100-150x. 

![hp1_7subplot.png](https://bitbucket.org/repo/Mx7pKn/images/2061119558-hp1_7subplot.png)

Compare how the Harry Potter series progresses to the Maze Runner series. As shown in the plot below, there is a main character that is mentioned over 1000 times throughout the novels. The number of main characters in this series actually shrinks as the series progresses. Unlike the Harry Potter series, where minor characters are increasingly developed into main characters, the Maze Runner series focuses on the protagonist alone and does not provide character depth to anyone else in the book. 

![mazerunner1_3subplots.png](https://bitbucket.org/repo/Mx7pKn/images/625874408-mazerunner1_3subplots.png)

Already, the data is starting to reveal how character breadth and depth varies for different novels. Next, I wanted to explore this concept over the progression of a novel and over the progression of a series.

### Final Approach ###

In order to better understand character depth and breadth in a given series of books, I refined my initial approach so that I could look at the number of characters in each chapter throughout a series. I also refined the data by plotting separate bars based on the number of times each character was mentioned in the chapter. Specifically, the grey bars in the plots below show the total number of characters mentioned in each chapter (including very minor characters). The red bars filter out characters who were mentioned less than 3 times. The blue bars represent dominant characters in the chapter, and filter out characters who were mentioned less than 15 times. 

Before I looked at the data from the remaining epubs, I made a list of the books which I planned to analyze. Then I ranked them in order of how much I liked that book. In order of my most to least favorite:

* Harry Potter series by J.K. Rowling
* Brotherband chronicles by John Flanagan tied with the Beyonders series by Brandon Mull
* Hunger Games series by Suzanne Collins
* Maze Runner series by James Dashner
* Divergent series by Veronica Roth (I couldn't even bear finishing this series)

Notably, for each series, I tried to use the NLTK library to tag all proper pronouns in a given book, in an attempt to extract a list of all characters in the book (after all, I don't remember all the minor characters from books that I read 5 years ago). I found out that the library was unable to successfully tag all of the proper pronouns. I did not expect the code to be able to distinguish between places and names ("Hogwarts" and "Harry" are both proper pronouns). I was disappointed to find that the code was tagging random words like "Please" and "Unless" which are definitely not proper pronouns. I attempted to also filter out tagged words which occurred less than 4 times. This assumes that characters who are only mentioned 3 times are insignificant to the story (i.e., I do not even consider them to be minor characters). In the end, I had to do a lot of manual editing. I sorted the output by frequency of occurrence, and deleted words from the bottom of the list which were clearly not names. For all words that I was unsure of, I looked each up online to figure out if it was actually a character or not. For instance "Felrook" from the Beyonders series is a location, not a person (and I could not remember this).

## Key Results ##

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

## Conclusions ##
The preliminary results show that there are indeed some trends in the style of storytelling that I prefer. I like the Harry Potter books the most, and perhaps that means I enjoy novels with impressive character breadth. There are several reasonable explanations for why I might appreciate breadth. I may find that the Harry Potter books are closer to reality because I know a great deal more than 20 people. In fact, I interact with many people per day, and so the large number of characters present in the Harry Potter books agrees with how I feel people interact with others on regular basis. The Harry Potter books are not without character depth, however. There are apparent "dips" in the data, which occur more and more frequently as the series progresses. I think these dips represent chapters in which the author chooses to provide additional depth to new characters.

The Beyonders and Brotherband books are actually pretty different. There isn't a lot of character "noise" in the Beyonders series, and the blue bars are relatively large compared to the grey bars. This shows me that the Beyonders series probably has a lot of character depth. The Brotherband books have a more even distribution of blue, red, and grey. Interestingly, the Divergent series (my least favorite books) have the smallest blue bars, indicating that the character depth may be lacking. I have made a lot of assumptions here, however, and this analysis could be improved.

## Assumptions ##

* When creating the character lists, I deleted last names and prefaces such as "Professor" to avoid double counting. The assumption here is that characters are usually referred to by one name more than the other.  This also helps to avoid confusion over shared family names.
* There is some error in creating the list of characters in a series. I ignored characters that were only mentioned < 5 times. 
* There is a subtle assumption that chapter lengths are more or less similar across a particular book, and across different series. I describe this assumption as "subtle" only because I am *comparing* different series. For instance, the Maze Runner series has a lot more chapters than some of the other novels I analyzed. If the chapters are shorter, perhaps this means the cutoff for the blue and red bars should be different.

## Future Work ##

* Add more books, including fiction outside the scope of "young adult."
* Create interactive plots to make the data easier to digest.