# Milestone 3

## Description of Project

Ash's Movie Explorer is a web application that randomizes a movie and its details everytime the page is reloaded. The details (title, tagline, genres, movie poster image, and Wikipedia article link) are dynamically fetched using the TMDB and Wikipedia API. The web application is served via the flask framework, and deployed on Heroku. In addition, I added a login/register page that allows a user to login and register for the movie explorer. Lastly, there is a new section on every movie allowing for an addition of ratings and comments, and another page that allows you to delete/edit comments/ratings. 

## Layout of Project

The contents of this web application include "static" and "templates" directories. The CSS components (style.css and external images) are found within the static directory. The templated directory now contains 3 HTML pages: login.html, register.html, index.html. In addition, the project directory includes app.py, tmdb.py, a Procfile, requirements.txt, a .env file, and a .gitignore file. The flask framework is running in app.py, whereas the API fetching is done in my api.py file. In addition, we use flask SQLALCHEMY in order to connect to our Heroku Database. 

### Using Flask

Within this file I imported these libraries: os, random, flask, requests, and tmdb (get_title, get_tagline, get_genre, get_image, get_wiki_page). 
* I used the os library to help hide my API key in a .env file. 
* I used random to help pick a random movie id from the list. 
* I used flask to help create the web application, route it to the correct place, and connect it to the HTML page. 
* The requests library allows us to send HTTP requests using python. 
* I also needed to import all the methods written for API calls into app.py so they could be easily called and rendered to the HTML file. 
* I used flask_sqlalchemy to get SQLAlchemy, the extension for flask that makes it simple to do commmon tasks with a database in python. 
* I used flask_login and its classes, methods, variables in order to provide user session management for my project. 

I have two methods in this file: get_random_movie and get_movie. get_random_movie randomizes the movie id and builds the movie base url and configures the json. It is then called in get_movie (the routed function). In this function, we return flask.render_template which sends all my method calls to the HTML file. We then call app.run and include a host and a port so it can be deployed in Heroku.

### API Fetching

Within this file I imported these libraries: os, requests, dotenv (load_dotenv, find_dotenv). 
* I used the os library to help hide my API key in a .env file. 
* I used the dotenv library to call the methods listed above to help recognize my API key from the .env file, so the file will call the APIs as intended. 
* The requests library allows us to send HTTP requests using python. 

I created a separate function for each piece of information we were fetching for the TMDB Movie API. This resulted in 4 methods: get_title, get_tagline, get_genre, get_image. Using the movie json response (made in app.py), we can easily filter through the JSON to find the title and tagline. The genres were a bit more complicated because the output was a list of dictionaries, so it needed to be looped through and picked the value from the key-value pair. For the movie poster, I had to use the configuration API and build the final url from the base_url + size + poster_path. 

The last function in this file is get_wiki_page (calls information from Wiki API). I constructed the Wikipedia article url from the link and the movie title that was passed through as a query parameter from the get_title function above. 

### Heroku
The application is deployed on Heroku. We created a heroku database in order to store information for the application. The application can be found at: https://vast-forest-34825.herokuapp.com/ (FROM MILESTONE 2)

## Main Changes in Milestone 3

### React Page
On the main movie page, the user has the option to click a button to edit/delete their commments. This button takes you to a React page which utilizes useState hooks. It contains a useEffect() hook that uses the fetch method to get JSON data and passes it through setComment(). I created two functions: deleteReview() and saveAllChanges(). DeleteReview removes a comment from the list (just from the UI, not the DB). SaveAllChanges() takes in a request and fetches JSON data from an endpoint we created within app.py. This endpoint deletes all comments from the current user and adds back only the ones remaining on the UI. It also alerts when changes have been saved. I pass through all the comments and their attributes through the return statement of the React page. 
* I imported { useState, useEffect } from 'react'

## Answered Questions

### How to run locally?

#### Install general libraries
1. pip install python-dotenv
2. pip install requests
3. pip install flask
#### PostgreSQL Setup
5. brew install postgresql (if on mac)
6. brew services start postgresql (if on mac)
7. psql -h localhost  # this is just to test out that postgresql is installed okay - type "\q" to quit
8. pip install psycopg2-binary
9. pip install Flask-SQLAlchemy==2.1
10. pip install flask-login
#### Heroku Setup
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)  # install Homebrew
brew tap heroku/brew && brew install heroku  # install Heroku CLI
#### Adding to the .env file
You would need to create a .env file within the project and add
* export REALDATABASE_URL="name of your url"
* add a new API key... API_KEY="your api key"
* add a new secret key...app.secret_key="name of your secret key"
#### How to make database
* git init, add + commit all changed files with git
* heroku login -i
* heroku create
* heroku addons:create heroku-postgresql:hobby-dev
* heroku config -- to get database_url and change it to REALDATABASE_URL and change postgres to postgresql
#### Install React/Node
* brew update
* brew install node
* sudo apt install npm, pip install npm
* npm install react
#### How to run app
* npm ci
* npm run build
* Then, type python or python3 app.py into your terminal once you are within the correct directory


### What was the hardest part of the project for you? Most valuable learning of overall project?
* The hardest part was byfar Milestone 3. I feel like I had a bad grasp and understanding going into Milestone 3 and would have liked extra time for this project. Also, React felt very abstract to me and I did not get enough practice in. I was able to follow in the demos but combining it with the database was definitely the hardest part of this project.
* I believe the most valuable part of this project was learning the API portion. It is a fundamental thing that I have been trying to practice, and it was rewarding to see my calls to the movie API work. I will be working with APIs this summer at my internship so I felt that was a huge takeaway for me. 

1. I expected the login/register part of this project to be the easiest part during planning. It seemed like a quick add to the database and a simple redirect. Although in hindsight that is all it is, I struggled a lot during this part of the project. I started off with my register page being the first thing seen. Although I planned for this, it made a lot more sense logically to start with the login and then go from there. I start with my login and have a hyperlink to register if the user wants to do so. From there, the user can register and be redirected automatically. Or the user can enter the login info right away and be redirected. 
2. Another planning gone wrong situation was my reviews/comments. I originally had planned for everything to be within the same table because it made more sense to have everything be called from one table. Soon realizing that was not going to work, I made two separate tables and that made things a lot simpler. I was trying to add the username from the user table in the comments table, but I could just add a current_username column in the comments table. This made using flask_login a lot simpler, and I better understand database schema more now. 

### Technical Issues and How I Solved Them

1. This project was byfar the hardest one for me. The first issue I ran into was creating an API endpoint that returned a full set of comments and connecting that to App.js. This took a lot of research and understanding, but I viewed some of the previous lectures and stackoverflows and understood we needed to query the DB per current user and grab all the comments from that. Then, the easiest way was to add each dictionary (JSON) to a list and use flask.jsonify. I also needed to grasp the understanding of useEffect and how we used fetch() to access that JSON data. 
2. Another issue I had for the longest time was getting one comment to delete from the UI, after displaying it on the screen. I had everything mapped correctly and was traversing through the list correctly, however I kept getting an error in which the correct row was deleting, however the input boxes remained in the same place. This gave the illusion that the wrong row was deleting from the list of comments. After struggling for hours, I realized I needed to set a key for the table I had created (key={list_all_comments.id}). 
3. The last issue I had was understanding how to update DB logic based on the save button. This took a lot of understanding and viewing the demo/lectures, and reading from external sites. My thinking was to create an endpoint in app.py that deleted all comments based on the current user, and then added back all comments on the screen (what was not deleted off the UI). I was able to mock a function created in milestone 2 for this, but had trouble translating it to the App.js. It was printing the correct flask.request.json for me, however I was passing through my state variable id, when I meant to pass through just my state variable.  
