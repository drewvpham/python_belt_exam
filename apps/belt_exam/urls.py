from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^quotes$', views.quotes, name='quotes'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^create_quote$', views.create_quote, name='create_quote'),
    url(r"^users/(?P<id>\d+)", views.users, name='users'),
    url(r"^add_favorite/(?P<id>\d+)", views.add_favorite, name='add_favorite'),
    url(r"^remove_favorite/(?P<id>\d+)", views.remove_favorite, name='remove_favorite'),
    url(r"^delete/(?P<id>\d+)", views.delete, name='delete'),
]
