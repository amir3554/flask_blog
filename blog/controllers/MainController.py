from flask import render_template, request, jsonify
from blog.forms.Forms import ArticleForm
from blog.models.Models import Article, Like
from blog.models.AuthModels import User, StripeCustomer
from blog import conf, db
from flask import redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from blog.utils.MainUtils import Paginate, is_admin_test
from blog.utils.ArticleUtils import save_image
 


def home():
    pagination, articles_per_page = Paginate(
        conf.ARTICLES_PER_PAGE,
        Article,
        (Article.created_at.desc())
        )
    
    return render_template(
        "main/home.html",
        title="hasoub-blog",
        articles_per_page=articles_per_page,
        pagination=pagination
        )


@login_required
@is_admin_test
def articles_list():
    pagination, articles_list = Paginate(
        conf.RECORD_PER_PAGE,
        Article,
        (Article.id.desc())
        )
    
    return render_template(
        "articles/articles_list.html",
        title="hasoub-blog",
        articles_list=articles_list,
        pagination=pagination
        )





def article(id):
    article = Article.query.get_or_404(id)
    if current_user.is_authenticated:
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer is not None:
            return render_template("articles/article.html", customer=customer, article=article, title=article.title)
    return render_template("articles/article.html", article=article, title=article.title)



@login_required
@is_admin_test
def article_add():
    form = ArticleForm()
    if form.validate_on_submit():

        if form.image.data:
            image_name = save_image(form.image.data)
        else:
            image_name = None
        article = Article(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            image=image_name
            )
        db.session.add(article)
        db.session.commit()
        flash("The Article was added successfully.", "success")
        return redirect(url_for('MainRoute.home'))
    return render_template('articles/article_add.html', form=form, legend="Add new article", title="Add article")



@login_required
@is_admin_test
def article_update(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)
    image_name = article.image
    form.existing_image.data = article.image

    if form.validate_on_submit():

        if form.image.data:
            image_name = save_image(form.image.data)
            article.image = image_name              

        article.title = form.title.data
        article.content = form.content.data
        article.image = image_name

        db.session.commit()

        flash("The Article was updated successfully.", "success")
        return redirect(url_for('ArticleRoute.article', id=article.id))
    
    form.title.data = article.title
    form.content.data = article.content
    form.image.data = article.image

    return render_template(
        'articles/article_add.html',
        form=form,
        legend="update article",
        title="update article"
        )



@login_required
@is_admin_test
def article_delete(id):  
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("The Article was successfully deleted", "success")
    return redirect(url_for('ArticleRoute.articles_list'))



@login_required
def article_like(id):
    if request.method == "GET":
        flash("An error occured, try again.")
        return redirect(url_for("ArticleRoute.article", id=id))
    
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    if (customer is None or customer.status != "active") and (not current_user.is_admin):
        flash("Subscribe first to like this article.")
        return redirect(url_for("ArticleRoute.article", id=id))

    article = Article.query.get_or_404(id)
    like = Like.query.filter_by(liked_article=article.id, liked_user=current_user.id).first()

    if like is not None:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(liked_article=article.id, liked_user=current_user.id)
        db.session.add(like)
        db.session.commit()
    return jsonify(
        {
            'likes':len(article.likes),
            'liked':current_user.id in map(lambda l: l.liked_user, article.likes),#:bool
        }
    )



