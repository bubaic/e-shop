from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.shortcuts import reverse

from accounts.models import Guest
from fup.stripe_info import stripe

# Create your models here.

User = settings.AUTH_USER_MODEL

class BillingManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_id')
        obj = None
        created = False
        if user.is_authenticated:
            # if user.email:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
            # print(obj, created)
        elif guest_email_id is not None:
            guest_email_obj = Guest.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
            # print(obj, created)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.email

    objects = BillingManager()

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self): # gets all the cards available
        return self.card_set.all()

    @property
    def has_card(self): # if cards exists it'll return that
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self): # set default card & return it
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def get_payment_url(self):
        return reverse('billing:bill-pay')

    def set_card_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

def billing_profile_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print('API Request Send to stripe')
        customer = stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_receiver, sender=BillingProfile)

def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_reciever, sender=User)

class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_resp = customer.sources.create(source=token)
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=card_resp.id,
                brand=card_resp.brand,
                country=card_resp.country,
                exp_month=card_resp.exp_month,
                exp_year=card_resp.exp_year,
                last4=card_resp.last4
            )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id       = models.CharField(max_length=120)
    brand           = models.CharField(max_length=120, null=True, blank=True)
    country         = models.CharField(max_length=10, null=True, blank=True)
    exp_month       = models.IntegerField(null=True, blank=True)
    exp_year        = models.IntegerField(null=True, blank=True)
    last4           = models.CharField(max_length=4, null=True, blank=True)
    default         = models.BooleanField(default=True)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return f'{self.brand} - {self.last4}'

def new_card_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_receiver, sender=Card)

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available!"

        c = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency='usd',
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={
                'order_id': order_obj.order_id
            }
        )
        new_charge = self.model(
            billing_profile=billing_profile,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome['type'],
            seller_message=c.outcome.get('seller_message'),
            risk_level=c.outcome.get('risk_level')
        )
        new_charge.save()
        return new_charge.paid, new_charge.seller_message

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id       = models.CharField(max_length=120)
    paid            = models.BooleanField(default=False)
    refunded        = models.BooleanField(default=False)
    outcome         = models.TextField(null=True, blank=True)
    outcome_type    = models.CharField(max_length=120, null=True, blank=True)
    seller_message  = models.CharField(max_length=120, null=True, blank=True)
    risk_level      = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()

    def __str__(self):
        return f'{self.billing_profile} charged on stripe @{self.stripe_id}'