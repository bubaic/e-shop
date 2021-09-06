import configparser

# mailchimp settings
keys = configparser.ConfigParser()
keys.read('./.env')
mailchimp = keys['Mailchimp']

MAILCHIMP_API_KEY		= mailchimp.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER	= mailchimp.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID	= mailchimp.MAILCHIMP_EMAIL_LIST
