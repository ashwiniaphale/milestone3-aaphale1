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
The application is deployed on Heroku. We created a heroku database in order to store information for the application. The application can be found at: https://vast-forest-34825.herokuapp.com/

## Main Changes in Milestone 3

### React Page



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
#### How to run app
Type python or python3 app.py into your terminal once you are within the correct directory

### How implementing your project differed from your expectations during project planning?

1. I expected the login/register part of this project to be the easiest part during planning. It seemed like a quick add to the database and a simple redirect. Although in hindsight that is all it is, I struggled a lot during this part of the project. I started off with my register page being the first thing seen. Although I planned for this, it made a lot more sense logically to start with the login and then go from there. I start with my login and have a hyperlink to register if the user wants to do so. From there, the user can register and be redirected automatically. Or the user can enter the login info right away and be redirected. 
2. Another planning gone wrong situation was my reviews/comments. I originally had planned for everything to be within the same table because it made more sense to have everything be called from one table. Soon realizing that was not going to work, I made two separate tables and that made things a lot simpler. I was trying to add the username from the user table in the comments table, but I could just add a current_username column in the comments table. This made using flask_login a lot simpler, and I better understand database schema more now. 

### Technical Issues and How I Solved Them

1. A big technical barrier for me was using and incorporating flask login. I asked around a bit and someone pointed me towards a flask's documentation (searching flask-login online). That helped A LOT. I incorporated the necessary imports and default lines that needed to be in the code such as: login_manager.init_app(app). After this the logic needed to play a role. Once I realized what I was doing, it was very simple to just login_user after my conditional statement about being added to the database. I looked up on stack overflow ("how to login user using flask login") for an example of that as well, and attended the Wednesday workshop where someone helped me read through that code. I was even able to add a logout button :)
2. Another problem I had was a struggle to deploy to heroku. I had forgotten to put in my API_KEY and secret key within heroku and had searched awhile on the internet regarding my "Keyerror: title" error. I got that error a lot after Milestone 1 so it clicked that it was related to the API, and that was how I realized I never passed through my API key. Also, I recieved this error: sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres. I saw John's comment on discord about this, but was still confused. I asked someone to clarify what he meant by that and realized that I needed to rename DATABASE_URL and readd it to heroku because heroku was passing through postgres and not postgresql. 
