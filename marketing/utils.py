import requests, json, hashlib, re
from fup import mailchimp as M

def check_email(email):
    if not re.match(r'.+@.+\..+', email):
        raise ValueError("It's not a valid email address.")
    return email

def hashing_subscriber(email):
    check_email(email)
    email = email.lower().encode()
    m = hashlib.md5(email)
    return m.hexdigest()

class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = M.MAILCHIMP_API_KEY
        self.api_url = f'https://{M.MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
        self.list_id = M.MAILCHIMP_EMAIL_LIST_ID
        self.endpoint = f'{self.api_url}/lists/{self.list_id}'

    def get_member_url(self):
        return self.endpoint + '/members'

    def valid_stat(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError("Not a valid status")
        return status

    def change_subscription_status(self, email, status='unsubscribed'):
        hash_email = hashing_subscriber(email)
        endpoint = self.get_member_url() + '/' + hash_email
        data = {
            'status': self.valid_stat(status)
        }
        r = requests.put(endpoint, auth=('', self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def check_subscription_status(self, email):
        hash_email = hashing_subscriber(email)
        endpoint = self.get_member_url() + '/' + hash_email
        r = requests.get(endpoint, auth=('', self.key))
        return r.status_code, r.json()

    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed')

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed')

    def pending(self, email):
        return self.change_subscription_status(email, status='pending')

    def cleaned(self, email):
        return self.change_subscription_status(email, status='cleaned')