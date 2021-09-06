
'''
Stripe API Setup
'''
import stripe, configparser
config = configparser.ConfigParser()
config.read('./.env')
stripe_keys = config['Stripe']

stripe.api_key	= stripe_keys.STRIPE_API
STRIPE_PK		= stripe_keys.STRIPE_PK
