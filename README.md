# Sentiment Analysis of Queer and Trans Asian Pacific Islander Blogs

For my [Metis](https://www.thisismetis.com/data-science-bootcamps) NLP/unsupervised learning project, I did topic modeling and sentiment analysis on the [Gaysian Diaries](https://gaysiandiaries.com/) and [Gaysian Third Space](https://gaysianthirdspace.tumblr.com/) tumblr blog posts. 

I discovered a surprising result from my analysis: the sentiment scores for each topic were on average positive even for difficult topics like body image and racism. I dug deeper by doing a sectional sentiment analysis of the posts. I found that on average the final section was the most positive, whereas the beginning and middle sections were on average more neutral in sentiment. At a more granular level, sentences carrying negative sentiments tended to be more concentrated in the beginning and middle sections as exemplified by [Gaysian Diary Entry #5](https://gaysiandiaries.com/post/146774821405/diary-entry-5). This trend of blog posts ending on a positive, optimistic note helped explain why the overall sentiment scores for each topic were more positive than one would think. 

I believe this finding points to the resiliency of the queer and trans Asian Pacific Islander community, that depsite the difficulties the community faces, many hold hope for a better tomorrow. 

To learn more, see my [blog post](https://binhhoang.io/blog/queer-asian-blogs/). 

## Table of Contents

* [Visualizations](#visualizations)
* [Technologies](#technologies)
* [Metis](#metis)

## Visualizations

![sentiment trend by topic](https://user-images.githubusercontent.com/62628676/100010363-27c16300-2d9e-11eb-8919-455b522ac64b.png)
![t-SNE doc-topic clusters](https://user-images.githubusercontent.com/62628676/93692277-17032100-fabf-11ea-9a90-4ce7d3da2a0b.png)
![Sentiment map slide](https://user-images.githubusercontent.com/62628676/93692255-c12e7900-fabe-11ea-8774-238bdfafdf4f.png)

## Technologies

* Python 3.8
* BeautifulSoup 4.9.1
* MongoDB 4.4.0
* NLTK 3.5
* Spacy 2.3.2
* vaderSentiment 3.3.2
* Scikit-learn 0.23.1
* Pandas 1.0.5
* Numpy 1.18.5
* Seaborn 0.10.1
* Plotly 4.8.2

## Metis

[Metis](https://www.thisismetis.com/data-science-bootcamps) is a 12-week accredited data science bootcamp where students build a 5-project portfolio. 
