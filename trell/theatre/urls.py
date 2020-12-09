from django.conf.urls import  url
from django.urls import path
from . import views

app_name = "theatre"

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^signup/$', views.sign_up, name="signup"),
  url(r'^login/$', views.login, name="login"),
  url(r'^add_movie/$', views.add_movie, name="add_movie"),
  url(r'^add_timings/$', views.add_timings, name="add_timings"),
  url(r'^search/$', views.search, name="search_movie"),
  # url(r'^purchase/$', views.purchase_ticket, name="purchase_ticket"),
  url(r'purchase/$', views.purchase_ticket, name="purchase_ticket"),
  # creating a temporary url for testing
  url(r'^home/$', views.home, name="home"),
]