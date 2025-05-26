from flask import render_template, request
from blog.forms.Forms import ArticleForm
from blog.forms.AuthForms import RegisterForm, LoginForm
from blog.models.Models import Article, User
from blog import db, bcrypt
from flask import redirect, url_for, render_template, flash
from flask_login import login_required
 


def home():
    return render_template("main/home.html", title="hasoub-blog")


@login_required
def article_add():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(user_id=1, title=form.title.data, content=form.content.data, image=form.image.data)
        db.session.add(article)
        db.session.commit()
        flash("The Article was added successfully.", "success")
        return redirect(url_for('MainRoute.home'))
    return render_template('articles/article_add.html', form=form, legend="Add new article", title="Add article")



