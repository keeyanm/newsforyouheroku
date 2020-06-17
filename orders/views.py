from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import json
from django.contrib.auth.models import User
import feedparser
from orders.models import feed, preference, sector
from requests import get
from requests.exceptions import RequestException
import urllib.request
from urllib.request import urlopen
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
    
def log_error(e):
    print(e)

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

def remove_html_markup(s):
    s = str(s)
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def covid(request):
    url = 'https://www.worldometers.info/coronavirus/'
    response = simple_get(url)
    html = BeautifulSoup(response, 'html.parser')
    table = html.find(id= "main_table_countries_today")
    tablebody = table.find_all('tbody')
    rows = tablebody[0].find_all("tr")
    data = []
    for row in rows:
        tds = row.find_all("td")
        # data.append([remove_html_markup(tds[0]),tds[1],tds[2],tds[3],tds[4],tds[5],tds[6],tds[7],tds[8],tds[9],tds[10],tds[11],tds[12],tds[13]])
        data.append([remove_html_markup(tds[0]),remove_html_markup(tds[1])
        ,remove_html_markup(tds[2]),remove_html_markup(tds[3]),remove_html_markup(tds[4]),
        remove_html_markup(tds[5]),remove_html_markup(tds[6]),
        remove_html_markup(tds[8]),remove_html_markup(tds[9]),remove_html_markup(tds[10]),
        remove_html_markup(tds[11]),remove_html_markup(tds[12])
        ,remove_html_markup(tds[13]),remove_html_markup(tds[14])])
    context = {
        'data': data[8:],
        'continents': data[0:8]
    }
    return render(request, 'covid.html', context)
    #find covid scrapable website

