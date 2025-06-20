import stripe

# ضع هنا مفتاحك السري
stripe.api_key = "sk_test_51R9nuzQRHgr09PFm6msj8mMQrsxoxJfzv9xozYdet1w2vhv6ZcQt8W3J14uEqgO6YXiWdq3QvFA5t0HORjgFNuXd00DI2NG3cP"
# اختياري: لتثبيت نسخة API محددة
stripe.api_version = "2023-08-16"

def stripe_subscription_create(customer_id: str, price_id: str):
    """
    ينشئ اشتراك شهري للعميل المحدد على Price ID الممرر.
    يُرجع كائن الـ Subscription كاملاً، مع توسيع latest_invoice.payment_intent
    للتعامل مع 3D Secure أو أخطاء الدفع.
    """

    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        # يجعل الاشتراك ينتظر إضافة طريقة دفع قبل إتمامه
        payment_behavior="default_incomplete",
        # يخزن طريقة الدفع المُستخدمة تلقائيّاً للاشتراكات المستقبلية
        payment_settings={"save_default_payment_method": "on_subscription"},
        # نوسع هذا الحقل للحصول على PaymentIntent جاهز للواجهة الأمامية
        expand=["latest_invoice.payment_intent"],
    )
    return subscription

# مثال استخدام:
if __name__ == "__main__":    # استبدل بالعميل الفعلي
    customer = stripe.Customer.create(name='amir', email='amirdwikat@gmail.com')
    customer_id = customer.id     
    price_id = "price_1RU2woQRHgr09PFmL0hjcMA7"
    sub = stripe_subscription_create(customer_id, price_id)
    print("Created subscription:", sub.id)
    # إذا احتجت client_secret لـ JS frontend:
    pi = sub.latest_invoice.payment_intent
    print("PaymentIntent status:", pi.status, "| client_secret:", pi.client_secret)