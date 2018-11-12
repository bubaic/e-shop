from django.conf.urls import url
from .views import AccountHomeView

app_name = 'accounts'

urlpatterns = [
    url(r'^$', AccountHomeView.as_view(), name='acc_home'),
]