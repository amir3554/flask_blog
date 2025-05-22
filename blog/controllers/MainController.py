from flask import render_template


class MainController():
    def home():
        return render_template("main/home.html", title="hasoub-blog")
