from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/', views.register_exist),
    url(r'^register_email_exist/', views.register_email_exist),
    url(r'^login/$', views.login),
    url(r'^login_handle/', views.login_handle),
    url(r'^info/', views.info),
    url(r'^order_(\d+)/$', views.order),
    url(r'^site/$', views.site),
    url(r'^logout/$', views.logout),
    # url(r'^cart/$', views.cart),
]

