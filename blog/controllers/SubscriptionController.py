from flask import render_template, redirect, flash, url_for, request, jsonify
from flask_login import current_user, login_required
import stripe.webhook
from blog import conf, db
from blog.models.AuthModels import StripeCustomer
import stripe
from blog.utils.SubscripeUtils import stripe_subscription_create, handle_subscription_db
from blog.utils.MainUtils import random_numeric_string
import json


def strip_test():
    return render_template('stripe_test.html')

def get_publishable_key():
    return jsonify(publicKey=conf.STRIPE_PUBLISHABLE_KEY)


def webhook_received():
    request_data = json.loads(request.data)
    webhook_secret = conf.STRIPE_WEBHOOK_SECRET
    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret
            )
            data = event['data']
            event_type = event['type']
        except Exception as e:
            return "error during getting the webhook process."
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data["object"]

    if event_type == 'customer.subscription.updated' :
        handle_subscription_db(data_object)
        print(f'the subscription object was created {event.id}')
    elif event_type == 'invoice.paid':
        print('payment success')
    return jsonify({'status' : 'success'})



def subscription():
    if current_user.is_anonymous:
        return render_template('subscribe/subscription.html', pricing=conf.PRICES, title="Subscription")
    
    # customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    # if customer is not None:
    #     #flash("You can subscribe from you account page.", "warning")
    #     #return redirect(url_for('SubscriptionRoute.subscription'))
    #     return jsonify('You can subscribe from you account page.')
    else:
        return render_template('subscribe/subscription.html', pricing=conf.PRICES, title="Subscription")

def post_price_id():
    data = request.json
    price_id = data.get('priceId') #type:ignore
    if not price_id:
        return jsonify({ "error": "missing priceId " }), 400
    return price_id

@login_required
def subscription_create():
    if current_user.is_admin:
        flash('admin can not subscribe', 'warning')
        return redirect(url_for('MainRoute.home'))
    
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    if customer and customer.status == "active":
        flash('You can upgrade you subscription from you account page', 'warning')
        return redirect(url_for('MainRoute.home'))
    
    priceId = request.form.get('priceId')
    if not priceId:
        print('priceId was not gotten')
        
    #price_id = post_price_id()
    #if price_id:
    #   print('price id was posted')

    #try:
    if customer is None:
        new_customer = stripe.Customer.create(
            name=current_user.username,
            email=current_user.email
            )
        subscription = stripe_subscription_create(new_customer.id, priceId)
        customer_db = StripeCustomer(
            id = random_numeric_string(6),
            user_id=current_user.id,
            customer_id = new_customer.id,
            subscription_id = subscription.id,
            )
        db.session.add(customer_db)
        db.session.commit()

    if customer is not None:
        subscription = stripe_subscription_create(customer.customer_id, priceId)
        customer.subscription_id = subscription.id
        db.session.commit()
        sub_description = subscription["latest_invoice"]["lines"]["data"][0]["description"]
        priceId = subscription["items"]["data"][0]["price"]["id"]
        client_secret = subscription.latest_invoice.payment_intent.client_secret #type:ignore
        return render_template(
            'subscribe/payment.html',
            sub_description=sub_description,
            client_secret=client_secret,
            priceId=priceId,
        )
    return render_template('subscribe/payment.html')

    #except Exception as e:#An error accurred while attempting to pay 
        #flash(f'{e} an error occurred, please try again', 'warning')
        #return redirect(url_for('SubscriptionRoute.subscription'))

@login_required
def subscription_success():
    payment_intent_status = request.args.get('paymentIntentStatus')
    if payment_intent_status is None:
        flash('you can see your subscription details in your account page', 'warning')
        return redirect(url_for('AuthRoute.user_account'))
    elif payment_intent_status == "success":
        return render_template('subscribe/payment_success.html', title='subscribe success')
    else:
        flash('an error accurred during payment process, check your profile ', 'warning')
        return redirect(url_for('AuthRoute.user_account'))
    
