from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signin", views.signin_view, name="signin"),
    path("covid", views.covid, name="covid"),
    path("preferencechange", views.preferencechange, name="preferencechange"),
    path("<str:user>/give", views.give, name="give")
]
