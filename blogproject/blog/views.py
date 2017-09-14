from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import render
from models import BlogPost


def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template("blog/archive.html")
    c = Context({'posts': posts})
    return HttpResponse(t.render(c))


# def archive(request):
#     posts = BlogPost.objects.all()
#     context = {'posts': posts}
#     return render(request, 'bolg/archive.html', context)
