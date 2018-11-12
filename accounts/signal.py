from django.dispatch import Signal

user_logging_signal = Signal(providing_args=['instance', 'request'])