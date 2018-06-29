from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^query', views.query, name='query'),
    url(r'^profile',views.profile, name='profile'),
    url(r'^changepassword', views.changepw, name='changepassword'),
    url(r'^salary', views.salary, name='salary'),
    url(r'^staffquery', views.salary_staff_query, name='staffquery'),
    url(r'^manage', views.manage, name='manage'),
]