from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View

from .models import MarketingPreference
from .forms import MktPrefForm
from .utils import Mailchimp
from .mixins import CsrfExemptMixin
from fup.mailchimp import MAILCHIMP_EMAIL_LIST_ID as mcl

# Create your views here.
class MktPrefView(SuccessMessageMixin, UpdateView):
    form_class = MktPrefForm
    template_name = 'marketing/forms.html'
    success_url = '/settings/email/'
    success_message = 'Your email preferences have been updated. Thank You!'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/settings/email/')
            # return HttpResponse(
            #     "<h1>Forbidden</h1>"
            #     "<p><b>403.</b> You don't have permission to access this page without login.</p><hr>",
            #     status=403
            # )
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preference'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj

class MailChimpWebhookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(mcl):
            hook_type = data.get('type')
            email = data.get('data[email]')
            resp_stat, resp = Mailchimp().check_subscription_status(email)
            sub_stat = resp['status']

            is_sub, is_mc_sub = None, None
            if sub_stat == 'subscribed':
                is_sub, is_mc_sub = (True, True)
            elif sub_stat == 'unsubscribed':
                is_sub, is_mc_sub = (False, False)

            if is_sub is not None and is_mc_sub is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        mailchimp_msg=str(data),
                        subscribed=is_sub,
                        mc_subscribed=is_mc_sub
                    )
        return HttpResponse('<h2>Thank You.</h2>', status=200)