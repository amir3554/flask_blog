from faker import Faker
from flask_seeder import Seeder
import blog
from blog.models import Models
import random
import os
from datetime import timedelta



fake = Faker("ar_AA")


class SeedDb(Seeder):
    def add_user(self):
        names = [fake.unique.first_name() + " " + fake.unique.last_name() for i in range(blog.conf.ACCOUNT_COUNT)]
        emails = [fake.unique.email() for i in range(blog.conf.ACCOUNT_COUNT)]
        for name, email in zip(names, emails):
            #first_name, last_name = name.split(" ", 1)
            user = Models.User(
                first_name = name.rsplit(" ", 1)[0],
                last_name  = name.rsplit(" ", 1)[1],
                username = name,
                email = email,
                password = blog.bcrypt.generate_password_hash(blog.conf.USER_PASSWORD).decode('utf-8'),
                is_admin = fake.boolean(chance_of_getting_true=blog.conf.ADMIN_PERCENTAGE),
                join_date = fake.date_this_year()
            ) 
            print(user)
            blog.db.session.add(user)

    def add_article(self):
        admins = Models.User.query.filter_by(is_admin=True).all()
        images = []
        directory = os.fsencode(blog.conf.MEDIA_DIR)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith('png') or filename.endswith('jpg'):
                images.append(filename)
        for i in range(blog.conf.ARTICLE_COUNT):
            admin = random.choice(admins)
            image = random.choice(images)
            article = Models.Article(
                title = fake.sentence(nb_words=7),
                content = fake.paragraph(nb_sentences=200),
                image = image,
                created_at = fake.date_this_year(),
                user_id = admin.id
            )
            print(article)
            blog.db.session.add(article) 

    def add_customer(self):
        subscribers = Models.User.query.filter_by(is_admin=False).all()
        for i in range(blog.conf.CUSTOMER_COUNT):
            subscriber = random.choice(subscribers)
            subscribers.remove(subscriber)
            subscription_start = fake.date_between(start_date=blog.conf.START_DATE)
            customer = Models.StripeCustomer(
                user_id = subscriber.id,
                subscription_type = "monthly",
                status = "active",
                customer_id = fake.lexify(text="id_????????????"),
                subscription_id = fake.lexify(text="sub_????????????"),
                amount = 10,
                subscription_start = subscription_start,
                subscription_end = subscription_start + timedelta(days=30),
                subscription_canceled = False
            )
            print(customer)
            blog.db.session.add(customer)

    def add_likes(self):
        articles = Models.Article.query.all()
        subscribers = Models.StripeCustomer.query.filter_by(status="active").all()
        admins = Models.User.query.filter_by(is_admin=True).all()
        subscribers.extend(admins)
        
        for article in range(blog.conf.LIKES_COUNT):
            liked_user = random.choice(subscribers).id
            liked_article = random.choice(articles).id

            like = Models.Like(
                article = article,
                liked_user = liked_user,
            )
            blog.db.session.add(like)

    def run(self):
        self.add_article()
        self.add_customer()
        self.add_user()
        self.add_likes()