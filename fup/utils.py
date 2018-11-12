import random, string
from django.utils.text import slugify

'''
Generate a random string using python
'''
def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    new_order_id = "ECX" + random_string_generator(size=7).upper()
    K = instance.__class__
    qs_exists = K.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_order_id

def unique_slug_generator(instance, new_slug=None):
    '''
    :param instance: has a model with
    :param new_slug: field & a title char field
    :return:
    '''
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        randstr = random_string_generator(10)
        new_slug = f'{slug}-{randstr}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug