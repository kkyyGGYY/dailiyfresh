from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('blog.urls', namespace="blog")),
    url(r'^admin/', include(admin.site.urls)),
)
