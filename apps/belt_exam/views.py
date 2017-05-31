from django.shortcuts import render, redirect
from models import *
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('quotes'))
    return render(request, 'belt_exam/index.html')


def register(request):
    if request.method=='POST':
        check=User.objects.validCheck(request.POST)
        print check
        if check['valid']==True:
            user=User.objects.createUser(request.POST)
            request.session['user_id']=user.id
            return redirect(reverse('quotes'))
        for error in check['errors']:
            messages.error(request, error)
    return redirect(reverse('landing'))

def login(request):
    if request.method=='POST':
        logger=User.objects.logging_in(request.POST)
        if logger['valid']==True:
            request.session['user_id']=logger['user'].id
            return redirect(reverse('quotes'))
        else:
            for error in logger['errors']:
                messages.error(request, error)
    return redirect(reverse('landing'))

def quotes(request):
    if 'user_id' in request.session:
        user=User.objects.filter(id=request.session['user_id']).first()
        quotes=Quote.objects.all().order_by('-id')
        context={'quotes':quotes, 'user': user}
        return render(request, 'belt_exam/quotes.html', context)
    return redirect(reverse('landing'))

def create_quote(request):
    if request.method=='POST':
        check= Quote.objects.quoteValidate(request.POST)
        if check['valid']==True:
            user=User.objects.get(id=request.session['user_id'])
            new_quote=Quote.objects.create(submitter=user, writer=request.POST['writer'], content=request.POST['content'])
        for error in check['errors']:
            messages.error(request, error)
    return redirect(reverse('quotes'))


def users(request, id):
    if 'user_id' in request.session:
        user=User.objects.filter(id=id).first()
        context={'user':user}
        return render(request, 'belt_exam/users.html', context)
    return redirect(reverse('landing'))

def add_favorite(request, id):
    if request.method=='POST':
        add_quote=Quote.objects.filter(id=id).first()
        user=User.objects.get(id=request.session['user_id'])
        add_quote.favorited_by.add(user)
        print user.favorites.all
    return redirect(reverse('quotes'))

def remove_favorite(request, id):
    if request.method=='POST':
        remove_quote=Quote.objects.filter(id=id).first()
        user=User.objects.get(id=request.session['user_id'])
        remove_quote.favorited_by.remove(user)
        print user.favorites
    return redirect(reverse('quotes'))

def delete(request, id):
    if request.method=='POST':
        Quote.objects.filter(id=id).delete()
    return redirect(reverse('quotes'))

def logout(request):
    request.session.pop('user_id')
    return redirect(reverse('landing'))
