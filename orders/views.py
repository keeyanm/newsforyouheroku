from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import json
from django.contrib.auth.models import User
import feedparser
from orders.models import feed, preference, sector
# Create your views here.
news = []
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": "Login or Sign Up."})
    #either go to choose or dashboard
    #comment under for fast
    x = preference.objects.all()
    userl = ''
    sectorl = []
    count = 0
    for i in x:
        userl += (str(i.user) +',')
        sectorl.append(str(i))
    userl = userl.split(',')[0:-1]
    sectors = []
    tb = []
    for i in range(len(sectorl)):
        sectorl[i] = sectorl[i].replace(' ','')
        sectorl[i] = sectorl[i].replace('wantstosee','')
        for j in userl:
            if j in sectorl[i]:
                # num = len(j)
                # sectors.append(sectorl[i][num:])
                tb.append(sectorl[i])
    tb = list(dict.fromkeys(tb))
    for t in tb:
        if str(request.user)+"-" in t:
            x = t
    #have to get all sectors for the right user
    for i in userl:
        if i == str(request.user):
            #comment under for fast
            # feeds = feed.objects.all()
            # for i in feeds:
            #     #return HttpResponse(i)
            #     for j in range(len(feedparser.parse(str(i))['entries'])):
            #         news.append(feedparser.parse(str(i))['entries'][j])
            onum = x.find('-')
            x = x[onum+1:]
            y = len(x.split(','))
            f = [['Sports'], ['Business'], ['Politics'], ['Economics'], ['Celebrities'], ['Technology']]
            for i in feed.objects.all():
                for j in f:
                    if j[0] == str(i.area):
                        j.append(i.feed)
            context = {
                "user": request.user,
                'preference': x,
                'feeds': f,
                'num': y
            }
            return render(request, 'dashboard.html', context)
    context = {
        "user": request.user,
    }
    return render(request, 'choose.html', context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})

def signin_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    emailaddress = request.POST["email"]
    first_name = request.POST["first-name"]
    last_name = request.POST["last-name"]
    try:
        user = User.objects.create_user(username, emailaddress, password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
    except: 
        return render(request, "login.html", {"message": "That Username already Exists."})
    return render(request, "login.html", {"message": "You can login with your new account."})

def give(request, user):
    sectorsl = request.POST["sectors"].split(',')
    p = preference.objects.create(user = request.user)
    for i in sectorsl:
        p.sectors.add(sector.objects.get(sector=i))
    p.save()
    # feeds = feed.objects.all()
    # for i in feeds:
    #     for j in range(len(feedparser.parse(str(i))['entries'])):
    #         news.append(feedparser.parse(str(i))['entries'][j])
    x = preference.objects.all()
    userl = ''
    sectorl = []
    count = 0
    for i in x:
        userl += (str(i.user) +',')
        sectorl.append(str(i))
    userl = userl.split(',')[0:-1]
    sectors = []
    tb = []
    for i in range(len(sectorl)):
        sectorl[i] = sectorl[i].replace(' ','')
        sectorl[i] = sectorl[i].replace('wantstosee','')
        for j in userl:
            if j in sectorl[i]:
                # num = len(j)
                # sectors.append(sectorl[i][num:])
                tb.append(sectorl[i])
    tb = list(dict.fromkeys(tb))
    for t in tb:
        if str(request.user)+"-" in t:
            x = t
    #have to get all sectors for the right user
    for i in userl:
        if i == str(request.user):
            #comment under for fast
            # feeds = feed.objects.all()
            # for i in feeds:
            #     #return HttpResponse(i)
            #     for j in range(len(feedparser.parse(str(i))['entries'])):
            #         news.append(feedparser.parse(str(i))['entries'][j])
            onum = x.find('-')
            x = x[onum+1:]
            y = len(x.split(','))
            f = [['Sports'], ['Business'], ['Politics'], ['Economics'], ['Celebrities'], ['Technology']]
            for i in feed.objects.all():
                for j in f:
                    if j[0] == str(i.area):
                        j.append(i.feed)
            context = {
                "user": request.user,
                'preference': x,
                'feeds': f,
                'num': y
            }
            return render(request, 'dashboard.html', context)
def preferencechange(request):
    f = preference.objects.all()
    for i in f:
        if str(i.user) == str(request.user):
            preference.objects.get(id=i.id).delete()
    context  = {
        'user': request.user
    }
    return render(request, "choose.html", context)
