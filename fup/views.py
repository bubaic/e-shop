from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .forms import ContactForm

User = get_user_model()

def home(request):
    ctx = {
        "title": "hello world!",
        "content": "Welcome to the homepage"
    }
    if request.user.is_authenticated:
        ctx['prm'] = 'Some premium content'
    return render(request, 'home_page.html', ctx)

def about_page(request):
    ctx = {
        "title": "About page",
        "content": "Welcome to about page"
    }
    return render(request, 'home_page.html', ctx)

def contact_page(request):
    form = ContactForm(request.POST or None)
    ctx = {
        'title': "Contact page",
        'content': "Welcome to contact page",
        'form': form
    }
    if form.is_valid():
        if request.is_ajax():
            return JsonResponse({
                'message': "Thank you for your submission! We'll get back to you shortly."
            })
    if form.errors:
        error = form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(error, status=400, content_type='application/json')
    return render(request, 'contact/contact_page.html', ctx)



