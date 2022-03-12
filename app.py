# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
# pylint: disable=trailing-newlines
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=global-variable-undefined
# pylint: disable=bad-whitespace
# pylint: disable=no-member
# pylint: disable=missing-class-docstring

import os
import random
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from api import get_title, get_tagline, get_genre, get_image, get_wiki_page

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("app.secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("REALDATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "default"

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.
bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# route for serving React page
@bp.route("/blueprintroute", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        # NB: DO NOT add an "index.html" file in your normal templates folder
        # Flask will stop serving this React page correctly
        return flask.render_template("index.html")
    return flask.render_template("index.html")


app.register_blueprint(bp)

# models
class UserTable(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.title}"


class CommentsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviews = db.Column(db.String(300))
    rating = db.Column(db.String(5))
    movie_id = db.Column(db.Integer)
    current_username = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Comments {self.title}"


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))


@app.route("/", methods=["GET"])
def default():
    return flask.redirect(flask.url_for("login"))


# start with default on login page
@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        user_form_data = flask.request.form.get("user_form")
        if (
            db.session.query(UserTable.id).filter_by(username=user_form_data).first()
            is not None
        ):  # if returns a user, then the username is already taken
            flask.flash("That username is already taken. Please try another one.")
        else:
            db.session.add(UserTable(username=user_form_data))
            db.session.commit()
            return flask.redirect(flask.url_for("get_movie"))

    return flask.render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        user_form_data = flask.request.form.get("user_form")
        if (
            UserTable.query.filter_by(username=user_form_data).first() is not None
        ):  # if the username is in the DB
            login_user(UserTable.query.filter_by(username=user_form_data).first())
            return flask.redirect(flask.url_for("get_movie"))  # go to movie page
        else:
            flask.flash("Invalid username, please register. ")
            return flask.redirect(flask.url_for("register"))  # otherwise go to register
    else:
        return flask.render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return flask.redirect("/login")


@app.route("/index", methods=["GET"])
@login_required
def get_movie():
    """calls functions from api and renders the output to flask"""
    favorite_movies = [
        313369,
        122906,
        27205,
        673,
        38757,
        2062,
    ]  # lalaland, about time, inception, HP, tangled, ratatouille
    random_movie_id = random.choice(
        favorite_movies
    )  # chooses random movie_id from the list
    all_comments = CommentsTable.query.filter_by(movie_id=random_movie_id).all()
    num_comments = len(all_comments)
    return flask.render_template(
        "main.html",
        movie_title=get_title(random_movie_id),
        movie_tagline=get_tagline(random_movie_id),
        movie_genre=get_genre(random_movie_id),
        movie_image=get_image(random_movie_id),
        movie_wiki=get_wiki_page(random_movie_id),
        all_comments=all_comments,
        num_comments=num_comments,
        random_movie_id=random_movie_id,
    )


@app.route("/review", methods=["GET", "POST"])
def comments():
    if flask.request.method == "POST":
        movie_reviews = flask.request.form.get(
            "review"
        )  # column name = data[form name]
        movie_ratings = flask.request.form.get("rating")
        movie_id = flask.request.form.get("movieID")
        now_user = current_user.username
        db.session.add(
            CommentsTable(
                reviews=movie_reviews,
                rating=movie_ratings,
                movie_id=movie_id,
                current_username=now_user,
            )
        )
        db.session.commit()
    return flask.redirect(flask.url_for("get_movie"))


@app.route("/reviewfromdb", methods=["GET", "POST"])
def commentEndPoint():
    logged_in_user = (
        current_user.username
    )  # logged in user should be the current user in DB
    full_comments = CommentsTable.query.filter_by(current_username=logged_in_user).all()
    comment_list = []
    for i in full_comments:
        comment_dict = {}
        comment_dict["id"] = i.id
        comment_dict["reviews"] = i.reviews
        comment_dict["movie_id"] = i.movie_id
        comment_dict["rating"] = i.rating
        comment_list.append(
            comment_dict
        )  # append each element of dictionary to the list
    return flask.jsonify(comment_list)


@app.route("/reviewfromid", methods=["GET", "POST"])
def getComments():
    if flask.request.method == "POST":
        CommentsTable.query.filter_by(
            current_username=current_user.username
        ).delete()  # this should delete everything from the db
        db.session.commit()  # in order to add back only what is shown on the UI
        new_request = flask.request.json
        print(new_request)
        for one_comment in new_request:  # copy of milestone 2 comments()
            rating = one_comment["rating"]
            reviews = one_comment["reviews"]
            movie_id = one_comment["movie_id"]
            db.session.add(
                CommentsTable(
                    reviews=reviews,
                    rating=rating,
                    movie_id=movie_id,
                    current_username=current_user.username,
                )
            )
            db.session.commit()

    return flask.redirect("/blueprintroute")  # should send it back to the App.js fetch


app.run(
    debug=True,
)
