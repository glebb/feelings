feelings
========

![feelings](https://raw.github.com/glebb/feelings/master/feelings.png)

feelings is a simple tool for gathering information about feelings of people. I have used it daily (part of our daily meetings) with my distributed team. After you have used it for a while, you can identify trends and use the information e.g. in retrospectives.

Live demo: http://displayofpatience.com:8080/

feelings is written in Python and Html5, and it saves the data to a simple sqlite db file. It uses http://flask.pocoo.org for server side stuff.

To install it, clone the repo and first install python requirements (requirements.txt). 

After installing the requirements you are ready to go. Execute "python tornado_server.py" to get it up and running. The app runs on port 8080 by default. Open http://your_computer_or_ip:8080/ on your browser to access it. You can also use "dev_server.py", especially if you plan to modify the source. It will run on localhost:5000 by default, and spits out errors, which comes in handy.

Basics:
  * feelings stores everything to a single-file db (feelings.sqlite). You can access it by any means, and process the data as you please. 
  * feelings web app provides following views: the main view (/) asks how you are doing today. By submitting the form the answer gets saved to the db. /show_avg displays averages by day including comments. /results displays a graph of averages with a "nikoniko" calendar view with individual answers color-coded day by day 
  * If you want to use feelings with multiple teams, you can define a category using a GET paramerter. Just append ?category=something at the end of the urls. E.g. http://localhost:8080/?category=team1 or http://localhost:8080/show_avg?category=team1 
  * TIP: you can use Excel to import data (set feelings /show_avg url as web data source and select the table with data) and to draw (nicer) graphs.
  
  ![nikoniko](https://raw.github.com/glebb/feelings/master/nikoniko.png)
  ![averages](https://raw.github.com/glebb/feelings/master/averages.png)
  