from django.conf import settings
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_save

from .signal import object_viewed_signal
from accounts.signal import user_logging_signal
from django.shortcuts import redirect

from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

# Create your models here.
class ViewManager(models.Manager):
    def set_user(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('/')
        return user

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address      = models.CharField(max_length=220, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content_object} viewed on {self.timestamp}'

    objects = ViewManager()

    class Meta:
        ordering            = ['-timestamp']
        verbose_name        = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_typ = ContentType.objects.get_for_model(sender) # same as instance.__class__
    user = None
    if request.user.is_authenticated:
        user = request.user

    new_view = ObjectViewed.objects.create(
        user=user,
        content_type=c_typ,
        object_id=instance.id,
        ip_address=get_client_ip(request)
    )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user        = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address  = models.CharField(max_length=220, blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    ended       = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - session on {self.ip_address} at {self.timestamp}'

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended

def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user).exclude(id=instance.id)
        for i in qs:
            i.end_session()

post_save.connect(post_save_session_receiver, sender=UserSession)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

user_logging_signal.connect(user_logged_in_receiver)