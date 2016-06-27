# Using Data to Answer "What Makes a Good Story?" #

##Background##
How often do you hear someone asking "Have you read any good books lately?" Usually, the person asking this question has probably wasted hours of their life reading crappy books. When you login to amazon.com, you're given suggestions for what books you would like, based on the books you've already read. Unfortunately, their algorithm for finding interesting books seems to be limited to *I see you've read the Hunger Games ... here are some more Dystopian novels for you. Maybe you should try the Twilight series - it's also popular, young adult fiction.* Meh - not helpful. In reality, I like all sorts of books. I've read over 100 classic novels, and am a fan of Dostoyevsky, but I also enjoy reading Harry Potter and similar young adult fantasy. And just because I've enjoyed a couple books from a particular genre, doesn't mean I only want to read books from that genre! I would guess that a good story is independent of genre, and strikes a certain balance between character depth and character breadth. The catch here is that some people don't care about character breadth (think about The Metamorphosis by Franz Kafka, where the entire story is a window into the mind of a single character), and some people prefer books with enormous breadth (honestly, I couldn't keep track of the characters in One Hundred Years of Solitude).

##Hypothesis##
Quantifying patterns in stories, including character breadth versus character depth, can help you identify the types of books that you enjoy reading. In this way, data can help us answer the question of "what makes a good story?" (which is of course, dependent on the user's personal reading preferences but not necessarily dependent on genre). 

## Methodology ##

I used Python to extract data from several electronic books (epubs) within the broad category of "young adult fiction." I chose to focus on character patterns, and refined my approach as I continued to explore the results.

### Initial Approach ###
I started to explore the data by first looking at the Harry Potter series. This choice was driven by the online availability of a full character list for these books.

### Final Approach ###

Before I looked at the remaining epubs, I made a lit of the books which I planned to analyze. Then I ranked them in order of how much I liked that book. In order of my most to least favorite:

* Harry Potter series by J.K. Rowling
* Brotherband chronicles by John Flanagan
* Beyonders series by Brandon Mull
* Hunger Games series by Suzanne Collins
* Maze Runner series by James Dashner
* Divergent series by Veronica Roth (I couldn't even bear finishing this series)

## Key Results ##
![hp7_bychapter.png](https://bitbucket.org/repo/Mx7pKn/images/1879984733-hp7_bychapter.png)

![hungergames3.png](https://bitbucket.org/repo/Mx7pKn/images/848505291-hungergames3.png)

## Conclusions ##
The preliminary results show that 

## Assumptions ##

* When creating the character lists, I deleted last names and prefaces such as "Professor" to avoid double counting. The assumption here is that characters are usually referred to by one name more than the other.  This also helps to avoid confusion over shared family names.

## Future Work ##

* Add more books, including fiction outside the scope of "young adult."
* Create interactive plots to make the data easier to digest.