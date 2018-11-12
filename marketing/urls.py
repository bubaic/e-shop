from django.conf.urls import url
from .views import MktPrefView

app_name = 'marketing'

urlpatterns = [
    url(r'^settings/email/$', MktPrefView.as_view(), name='mkt-pref'),
]