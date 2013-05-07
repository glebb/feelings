feelings
========

![feelings](https://raw.github.com/glebb/feelings/master/feelings.png)

feelings is a simple tool for gathering information about the feelings of people. You can use the data it gathers 
to draw a happiness index for example. I use it daily (part of our daily meetings) with my distributed team, so I get an overall view on what's going on in our team.

feelings is written in Python, and it saves the data to a simple sqlite db file. It uses http://flask.pocoo.org for server side stuff.

To install it, clone the repo and install requirements: pip install -r requirements.txt 

Then you can simply start the development server, or run it via Apache or by some other means. I use http://gunicorn.org.
Check Flask documentation for more information.

Basics:
  * feelings stores everything to a single table. If you want to use it with multiple teams, you can define a category using a GET paramerter. Just append e.g. /?category=team2 at the end of the url in the main page.
  * To display results in a web page, use /show_data and /show_avg. To display results for a specific team/category, add GET parameter (e.g. /show_avg?category=team2). Currently it only shows numbers (see TODO). 

TODO:
  * Draw graphs based on gathered data.
