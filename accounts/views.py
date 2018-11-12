from django.contrib.auth import authenticate, logout, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegisterForm, GuestForm
from .models import Guest
from .signal import user_logging_signal

User = get_user_model()

# Create your views here.

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    ctx = {
        'form': form
    }
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest = Guest.objects.create(email=email)
        request.session['guest_id'] = new_guest.id
        # user_logging_signal.send(user.__class__, instance=user, request=request)
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect('/register/')

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     ctx = {
#         'form': form
#     }
#     next_get = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_get or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 print('redirect_path: ', redirect_path, 'next host: ', request.get_host())
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print("error")
#     return render(request, 'auth/login_page.html', ctx)

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     ctx = {
#         'form': form
#     }
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         email = form.cleaned_data.get('email')
#         newuser = User.objects.create_user(username, email, password)
#         print(newuser)
#     return render(request, 'auth/register.html', ctx)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/login/'

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'auth/login_page.html'

    def form_valid(self, form):
        request = self.request
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=email, password=password)

        # ''' excluding some invalid emails '''
        # emails_to_exclude = ['@example.com', '@test.com', '@mailinator.com' ....]
        #     users = Users.objects
        #     for exclude_email in emails_to_exclude:
        #         users = users.exclude(email__endswith=exclude_email)
        #     users = users.all()

        if user is not None:
            login(request, user)
            user_logging_signal.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        user_logging_signal.send(instance=None, request=request, sender=user)
        return super().form_invalid(form)